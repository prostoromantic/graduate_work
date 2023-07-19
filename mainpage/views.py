from .forms import FabricatorForm, ParameterForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.template import RequestContext
from .models import Counties, Statistic, Fabricator, Material


def page_not_found_view(request, exception):
    return render(request, 'mainpage/page_404.html', status=404)


def index(request):
    return render(request, 'mainpage/index.html')


def graphics(request, graphic_type):
    if graphic_type == 'Средняя выручка':
        counties_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                counties_list.append(int(label.split('_')[1]))
        revenues = Statistic.objects.all()
        data, counties, series = {}, {}, {}
        for revenue in revenues:
            if revenue.county.id in counties_list or len(counties_list) == 0:
                if not revenue.county.county_name in data:
                    data[revenue.county.county_name] = [revenue.revenue]
                else:
                    data[revenue.county.county_name].append(revenue.revenue)
                if revenue.county.county_name in series:
                    series[revenue.county.county_name]['data'].append([
                        revenue.fabricator.fabricator_name, int(revenue.revenue)
                    ])
                else:
                    series[revenue.county.county_name] = {
                        'name': revenue.county.county_name,
                        'id': revenue.county.county_name,
                        'data': [
                            [revenue.fabricator.fabricator_name, int(revenue.revenue)]
                        ]
                    }
            if not revenue.county.county_name in counties:
                counties[revenue.county.county_name] = revenue.county.id
        series = [series[c] for c in list(series.keys())]
        for i in range(len(series)):
            series[i]['data'] = sorted(series[i]['data'], key=lambda x: x[1])
        render_data = {'country_data': [], 'counties': [], 'series': series}
        for county in data:
            render_data['country_data'].append({
                'name': county,
                'y': int(sum(data[county]) / len(data[county])),
                'drilldown': county
            })
        for county in counties:
            if county in data:
                render_data['counties'].append([county, counties[county], True])
            else:
                render_data['counties'].append([county, counties[county], False])
        return render(request, 'mainpage/graphic_average_revenue.html', context=render_data)
    elif graphic_type == 'Число работников':
        revenues = Statistic.objects.all()
        material_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                material_list.append(int(label.split('_')[1]))
        data, fabrics = {}, []
        for revenue in revenues:
            if revenue.material.id in material_list or len(material_list) == 0:
                if not revenue.county.county_name in data:
                    data[revenue.county.county_name] = [[revenue.fabricator.fabricator_name, revenue.workers]]
                else:
                    data[revenue.county.county_name].append([revenue.fabricator.fabricator_name, revenue.workers])
                if not revenue.material.material_name in [fabric[0] for fabric in fabrics]:
                    fabrics.append([revenue.material.material_name, revenue.material.id, True])
            else:
                if not revenue.material.material_name in [fabric[0] for fabric in fabrics]:
                    fabrics.append([revenue.material.material_name, revenue.material.id, False])
        for key in data:
            data[key] = sorted(data[key], key=lambda x: x[1])
        return render(request, 'mainpage/graphic_count_workers.html', context={'data': data, 'fabrics': fabrics})
    elif graphic_type == 'Выручка предприятий':
        revenues = Statistic.objects.all()
        revenue_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                revenue_list.append(int(label.split('_')[1]))
        data, revenues_list = {}, []
        for revenue in revenues:
            if revenue.material.id in revenue_list or len(revenue_list) == 0:
                if not revenue.county.county_name in data:
                    data[revenue.county.county_name] = [[revenue.fabricator.fabricator_name, revenue.revenue]]
                else:
                    data[revenue.county.county_name].append([revenue.fabricator.fabricator_name, revenue.revenue])
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, True])
            else:
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, False])
        for key in data:
            data[key] = sorted(data[key], key=lambda x: x[1])
        return render(request, 'mainpage/graphic_revenue.html', context={'data': data, 'fabrics': revenues_list})
    elif graphic_type == 'Выручка на одного работника':
        revenues = Statistic.objects.all()
        revenue_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                revenue_list.append(int(label.split('_')[1]))
        data, revenues_list = {}, []
        for revenue in revenues:
            if revenue.material.id in revenue_list or len(revenue_list) == 0:
                if revenue.workers != 0:
                    if not revenue.county.county_name in data:
                        data[revenue.county.county_name] = [[revenue.fabricator.fabricator_name, round(revenue.revenue / revenue.workers, 2)]]
                    else:
                        data[revenue.county.county_name].append([revenue.fabricator.fabricator_name, round(revenue.revenue / revenue.workers, 2)])
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, True])
            else:
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, False])
        for key in data:
            data[key] = sorted(data[key], key=lambda x: x[1])
        return render(request, 'mainpage/graphic_coefficient_revenue.html', context={'data': data, 'fabrics': revenues_list})
    elif graphic_type == 'Выручка на индикативную силу':
        revenues = Statistic.objects.all()
        revenue_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                revenue_list.append(int(label.split('_')[1]))
        data, revenues_list = {}, []
        for revenue in revenues:
            if revenue.material.id in revenue_list or len(revenue_list) == 0:
                if revenue.indicative_forces != 0:
                    if not revenue.county.county_name in data:
                        data[revenue.county.county_name] = [[revenue.fabricator.fabricator_name, round(revenue.revenue / revenue.indicative_forces, 2)]]
                    else:
                        data[revenue.county.county_name].append([revenue.fabricator.fabricator_name, round(revenue.revenue / revenue.indicative_forces, 2)])
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, True])
            else:
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, False])
        for key in data:
            data[key] = sorted(data[key], key=lambda x: x[1])
        return render(request, 'mainpage/graphics-coefficient-forces.html', context={'data': data, 'fabrics': revenues_list})
    elif graphic_type == 'Число индикативных сил':
        revenues = Statistic.objects.all()
        revenue_list = []
        for label in request.GET:
            if request.GET.get(label) == 'on':
                revenue_list.append(int(label.split('_')[1]))
        data, revenues_list = {}, []
        for revenue in revenues:
            if revenue.material.id in revenue_list or len(revenue_list) == 0:
                if not revenue.county.county_name in data:
                    data[revenue.county.county_name] = [[revenue.fabricator.fabricator_name, revenue.indicative_forces]]
                else:
                    data[revenue.county.county_name].append([revenue.fabricator.fabricator_name, revenue.indicative_forces])
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, True])
            else:
                if not revenue.material.material_name in [fabric[0] for fabric in revenues_list]:
                    revenues_list.append([revenue.material.material_name, revenue.material.id, False])
        for key in data:
            data[key] = sorted(data[key], key=lambda x: x[1])
        return render(request, 'mainpage/graphic_ind_power.html', context={'data': data, 'fabrics': revenues_list})
    elif graphic_type == 'Сравнение двух предприятий':
        if request.method == 'POST':
            fabricator_1 = request.POST['form_1-fabricator']
            fabricator_2 = request.POST['form_2-fabricator']

            form_1 = FabricatorForm(request.POST, prefix='form_1')
            form_2 = FabricatorForm(request.POST, prefix='form_2')
            if form_1.is_valid() and form_2.is_valid():
                if fabricator_1 == fabricator_2:
                    return render(request, 'mainpage/graphic_comparison.html',
                                  context={'form_1': form_1, 'form_2': form_2,
                                           'error': 'Выберите двух разных предпринимателей!',
                                           'result': False})
                else:
                    fabricator_info_1 = Statistic.objects.filter(id=fabricator_1)[0]
                    fabricator_info_2 = Statistic.objects.filter(id=fabricator_2)[0]

                    fabricator_info_1 = {
                        'fabricator': fabricator_info_1.fabricator.fabricator_name,
                        'county': fabricator_info_1.county.county_name,
                        'material': fabricator_info_1.material.material_name,
                        'revenue': int(fabricator_info_1.revenue),
                        'indicative_forces': int(fabricator_info_1.indicative_forces),
                        'workers': int(fabricator_info_1.workers)
                    }
                    fabricator_info_2 = {
                        'fabricator': fabricator_info_2.fabricator.fabricator_name,
                        'county': fabricator_info_2.county.county_name,
                        'material': fabricator_info_2.material.material_name,
                        'revenue': int(fabricator_info_2.revenue),
                        'indicative_forces': int(fabricator_info_2.indicative_forces),
                        'workers': int(fabricator_info_2.workers)
                    }
                return render(request, 'mainpage/graphic_comparison.html', context={'form_1': form_1, 'form_2': form_2,
                                                                                    'fabricator_info_1': fabricator_info_1,
                                                                                    'fabricator_info_2': fabricator_info_2})
        else:
            form_1 = FabricatorForm(prefix='form_1')
            form_2 = FabricatorForm(prefix='form_2')
        return render(request, 'mainpage/graphic_comparison.html', context={'form_1': form_1,
                                                                            'form_2': form_2,
                                                                            'result': False})
    elif graphic_type == 'Анализ показателей':
        if request.method == 'GET':
            form_1 = ParameterForm(prefix='form_1')
            form_2 = ParameterForm(prefix='form_2')
            return render(request, 'mainpage/graphic_parameters.html', context={
                'graphic': False, 'form_1': form_1, 'form_2': form_2, 'error': False
            })
        elif request.method == 'POST':
            form_1 = ParameterForm(request.POST, prefix='form_1')
            form_2 = ParameterForm(request.POST, prefix='form_2')

            parameter_1 = request.POST['form_1-parameters']
            parameter_2 = request.POST['form_2-parameters']

            if parameter_1 == parameter_2:
                return render(request, 'mainpage/graphic_parameters.html', context={
                    'graphic': False, 'form_1': form_1, 'form_2': form_2,
                    'error': 'Выберите 2 разных параметра!'
                })

            renames = {
                'revenue': 'Выручка',
                'workers_count': 'Количество работников',
                'indicative_forces': 'Число индикативных сил'
            }

            data = []

            values = Statistic.objects.all()
            for value in values:
                if parameter_1 == 'revenue' and parameter_2 == 'workers_count':
                    data.append(
                        {
                            'x': value.revenue,
                            'y': value.workers,
                            'z': value.indicative_forces,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )
                elif parameter_1 == 'revenue' and parameter_2 == 'indicative_forces':
                    data.append(
                        {
                            'x': value.revenue,
                            'y': value.indicative_forces,
                            'z': value.workers,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )
                elif parameter_1 == 'workers_count' and parameter_2 == 'revenue':
                    data.append(
                        {
                            'x': value.workers,
                            'y': value.revenue,
                            'z': value.indicative_forces,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )
                elif parameter_1 == 'workers_count' and parameter_2 == 'indicative_forces':
                    data.append(
                        {
                            'x': value.workers,
                            'y': value.indicative_forces,
                            'z': value.revenue,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )
                elif parameter_1 == 'indicative_forces' and parameter_2 == 'revenue':
                    data.append(
                        {
                            'x': value.indicative_forces,
                            'y': value.revenue,
                            'z': value.workers,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )
                elif parameter_1 == 'indicative_forces' and parameter_2 == 'workers_count':
                    data.append(
                        {
                            'x': value.indicative_forces,
                            'y': value.workers,
                            'z': value.revenue,
                            'name': value.fabricator.fabricator_name[:2],
                            'full_name': value.fabricator.fabricator_name,
                            'place': value.county.county_name
                        }
                    )

            renames_copy_dict = renames.copy()
            renames_copy_dict.pop(parameter_1)
            renames_copy_dict.pop(parameter_2)

            return render(request, 'mainpage/graphic_parameters.html', context={
                'graphic': True, 'form_1': form_1, 'form_2': form_2, 'data': data,
                'param_1': renames[parameter_1], 'param_2': renames[parameter_2], 'param_3': renames[
                    list(renames_copy_dict.keys())[0]
                ], 'error': False
            })


def about(request):
    return render(request, 'mainpage/about.html')


def database(request):
    return render(request, 'mainpage/database_list.html')


def database_info(request, model, title):
    objects_list = model.objects.all()
    paginator = Paginator(objects_list, 15)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    vars = dict(
        posts=objects,
        title=title
    )
    if title == 'Таблица уездов':
        return render(request, 'mainpage/database.html', vars)
    elif title == 'Виды производств':
        return render(request, 'mainpage/database_materials.html', vars)
    elif title == 'Список предприятий':
        return render(request, 'mainpage/database_fabricators.html', vars)
    elif title == 'Данные по производству':
        return render(request, 'mainpage/database_values.html', vars)


def entrepreneurs(request):
    if request.method == 'GET':
        fabricators = Statistic.objects.order_by('-info')
        return render(request, 'mainpage/entrepreneurs.html', context={'fabricators': fabricators})
    elif request.method == 'POST':
        if len(request.POST.get('search')) == 0:
            fabricators = Statistic.objects.all()
        else:
            fabricators = Fabricator.objects.filter(fabricator_name__iregex=request.POST.get('search'))
            fabricators_id = [fabricator.id for fabricator in fabricators]
            fabricators = Statistic.objects.filter(fabricator_id__in=fabricators_id)
        return render(request, 'mainpage/entrepreneurs.html', context={'fabricators': fabricators})


def entrepreneur_info(request, post_id):
    fabricators = Statistic.objects.filter(id=post_id)
    if len(fabricators) > 0:
        kf_1 = round(fabricators[0].revenue / fabricators[0].workers, 2)
        kf_2 = None
        if fabricators[0].indicative_forces != 0:
            kf_2 = round(fabricators[0].revenue / fabricators[0].indicative_forces, 2)
        return render(request, 'mainpage/entrepreneur_info.html', context={'fabricator': fabricators[0],
                                                                           'kf_1': kf_1,
                                                                           'kf_2': kf_2})
    else:
        return render(request, 'mainpage/page_404.html')


def find_manufacture(request):
    values = Statistic.objects.all()
    materials = Material.objects.all()
    counties = Counties.objects.all()
    max_revenue = max([value.revenue for value in values])
    max_workers = max([value.workers for value in values])
    max_forces = max([value.indicative_forces for value in values])
    if request.method == 'POST':
        revenue_from = request.POST['revenue_from']
        revenue_to = request.POST['revenue_to']
        workers_from = request.POST['workers_from']
        workers_to = request.POST['workers_to']
        forces_from = request.POST['forces_from']
        forces_to = request.POST['forces_to']
        values = Statistic.objects.filter(
            revenue__gte=revenue_from, revenue__lte=revenue_to, workers__gte=workers_from, workers__lte=workers_to,
            indicative_forces__gte=forces_from, indicative_forces__lte=forces_to
        )
        materials = list(set([value.material_name for value in materials]))
        counties = list(set([value.county_name for value in counties]))
        data = {}
        for county in counties:
            data[county] = {}
            for material in materials:
                data[county][material] = {'workers': 0}
        for value in values:
            data[value.county.county_name][value.material.material_name]['workers'] += value.workers
        table_data = []
        for key in data:
            table_row = [key]
            for material in materials:
                table_row.append(data[key][material]['workers'])
            table_row.append(sum([data[key][material]['workers'] for material in materials]))
            table_data.append(table_row)
        table_row = ['Итого']
        for i in range(len(materials)+1):
            sum_ = 0
            for row in table_data:
                sum_ += row[i+1]
            table_row.append(sum_)
        headers = ['Губерния']
        for material in materials:
            headers.append(material)
        headers.append('Итого')
        table_data.append(table_row)

        data = {}
        for county in counties:
            data[county] = {}
            for material in materials:
                data[county][material] = {'fabric': 0}
        for value in values:
            data[value.county.county_name][value.material.material_name]['fabric'] += 1
        table_data_fabric = []
        for key in data:
            table_row = [key]
            for material in materials:
                table_row.append(data[key][material]['fabric'])
            table_row.append(sum([data[key][material]['fabric'] for material in materials]))
            table_data_fabric.append(table_row)
        table_row = ['Итого']
        for i in range(len(materials)+1):
            sum_ = 0
            for row in table_data_fabric:
                sum_ += row[i+1]
            table_row.append(sum_)
        headers = ['Губерния']
        for material in materials:
            headers.append(material)
        headers.append('Итого')
        table_data_fabric.append(table_row)
        return render(request, 'mainpage/find_manufacture.html', context={
            'max_revenue': int(max_revenue), 'max_workers': int(max_workers), 'max_forces': int(max_forces),
            'table_data': table_data, 'request': 'POST', 'headers': headers, 'table_data_fabric': table_data_fabric,
            'revenue_from': revenue_from, 'revenue_to': revenue_to,
            'workers_from': workers_from, 'workers_to': workers_to,
            'forces_from': forces_from, 'forces_to': forces_to
        })
    else:
        return render(request, 'mainpage/find_manufacture.html', context={
            'max_revenue': int(max_revenue), 'max_workers': int(max_workers), 'max_forces': int(max_forces),
            'request': 'GET',
            'revenue_from': 0, 'revenue_to': int(max_revenue),
            'workers_from': 0, 'workers_to': int(max_workers),
            'forces_from': 0, 'forces_to': int(max_forces)
        })