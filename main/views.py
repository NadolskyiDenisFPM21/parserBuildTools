from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from sites.models import Site, SiteGoods
from goods.models import Goods, Direction
from .models import ParseReport
from .tasks import task
from .excelReport.excel_creater import ExcelCreater


@login_required(login_url='login')
def index(request):
    directions = Direction.objects.all()
    parse_reports = ParseReport.objects.all().order_by('-id')[:10]
    context = {'parse_reports': parse_reports, 'directions': directions}

    return render(request, 'index.html', context)


def format_data(direction_id):
    headers = [
        ["№", "Код виробника", "Номенклатура", "РЦЦ", "Кількість порушень", ],
        ["", "", "", "", "", ],
        ["", "", "", "", "", ],
    ]
    sites = Site.objects.filter(direction=direction_id).order_by('id')
    goods = list(Goods.objects.filter(directions=direction_id).order_by('id'))
    data = []

    for product in goods:
        data.append([product.id, product.sku, product.name, product.price, 0])

    for site in sites:
        headers[0].append(site.name.encode('utf-8'))
        headers[0].append("")
        headers[0].append("")
        headers[1].append("Ціна")
        headers[1].append("URL")
        headers[1].append("Відхилення")
        headers[2].append(f"Відхилення {site.difference_percent}%")
        headers[2].append("")
        headers[2].append("")

        for row in data:
            product = SiteGoods.objects.filter(goods__sku=row[1], site=site).first()
            print(row[1], product, site.name)
            if product:
                row.append([product.price_on_site, product.link, product.difference])
                if product.difference != 0:
                    row[4] += 1
            else:
                row.append(['', '', ''])

    return headers, data


def format_data_sheet2(direction_id):
    headers = [[
        "№", "IM", "Кількість номенклатури", "Кількість порушень", "Відсоток порушень"
    ]]

    sites = Site.objects.filter(direction=direction_id).order_by('id')
    data = []
    for i, site in enumerate(sites):
        data.append([i, site.name, site.get_goods().count(), site.difference_count(), f"{site.difference_percent}%"])

    return headers, data


def create_report(request, direction_id):
    report = ExcelCreater()
    report.create(*format_data(direction_id))
    report.create2(*format_data_sheet2(direction_id))
    excel_file = report.get_file()
    django_file = ContentFile(excel_file.getvalue(), 'Report.xlsx')

    direction = Direction.objects.get(id=direction_id)
    parse_report = ParseReport.objects.create(file=django_file, name='Report', direction=direction)
    parse_report.save()
    return redirect('index')


def download_report(request, file_id):
    try:
        parse_report = ParseReport.objects.get(id=file_id)
        format_date = parse_report.created_at.strftime('%d-%m-%Y %H-%M')
        response = HttpResponse(parse_report.file,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{parse_report.name} {parse_report.direction.name} {format_date}.xlsx"'
        return response
    except ParseReport.DoesNotExist:
        raise Http404('Файл не знайдено!')


def task_parse(request):
    task.delay()
    return JsonResponse({'status': True})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'login.html')
