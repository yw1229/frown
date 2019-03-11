from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from stark.utils.page import MyPage
from django.db.models import Q
from crm.models import *
import copy
import random


class ShowList(object):
    """
    展示类
    """

    def __init__(self, config_obj, data_list, request):

        self.config_obj = config_obj  # 当前查看表的配置类对象
        self.data_list = data_list
        self.request = request

        # 分页
        self.pagination = MyPage(request.GET.get("page", 1), self.data_list.count(), request, 10)
        self.page_queryset = self.data_list[self.pagination.start:self.pagination.end]

    def get_search_fields(self):

        ret = [{"field_str": item, "field_verbose_name": self.config_obj.model._meta.get_field(item).verbose_name} for
               item in self.config_obj.search_fields]

        return ret

    def get_new_actions(self):

        temp = []
        temp.extend(self.config_obj.actions)
        temp.append(self.config_obj.patch_delete)

        new_actions = []
        # print(self.config_obj.actions) # [patch_init,patch_delete]
        for func in temp:
            new_actions.append({
                "text": func.desc,
                "name": func.__name__
            })

        return new_actions  # [{"text":"价格初始化","name":patch_init}，{"text":"批量删除","name":patch_delete}]

    def get_headers(self):

        # header_list=["书籍名称","价格","人民出版社"，"操作"]   默认配置类：    ["PUBLISH"]
        header_list = []
        for field_or_func in self.config_obj.new_list_display():  # ["title","price","publish",edit]
            if callable(field_or_func):
                val = field_or_func(self.config_obj, is_header=True)
            else:
                if field_or_func == "__str__":
                    val = self.config_obj.model._meta.model_name
                else:
                    filed_obj = self.config_obj.model._meta.get_field(field_or_func)
                    val = filed_obj.verbose_name
            header_list.append(val)

        return header_list

    def get_body(self):
        # 构建数据表单部分
        new_data_list = []

        for obj in self.page_queryset:  # Queryset[book1,book2]
            temp = []

            for field_or_func in self.config_obj.new_list_display():  # # ["title","price","publish",edit]  ["__str__"]

                if callable(field_or_func):
                    val = field_or_func(self.config_obj, obj)
                else:
                    #   获取字段对象
                    try:
                        from django.db.models.fields.related import ManyToManyField
                        field_obj = self.config_obj.model._meta.get_field(field_or_func)
                        if isinstance(field_obj, ManyToManyField):
                            rel_data_list = getattr(obj, field_or_func).all()
                            l = [str(item) for item in rel_data_list]
                            val = ",".join(l)
                        else:
                            val = getattr(obj, field_or_func)  # obj.title
                            if field_or_func in self.config_obj.list_display_links:
                                _url = self.config_obj.get_change_url(obj)
                                val = mark_safe("<a href='%s'>%s</a>" % (_url, val))

                    except Exception as e:

                        val = getattr(obj, field_or_func)

                temp.append(val)  # ["python",122,"人民出版社"，<a href='/stark/app01/book/1/change/'>编辑</a>]

            new_data_list.append(
                temp)  # [["python",122,"人民出版社"，<a href='/stark/app01/book/1/change/'>编辑</a>]，["linux",123,"人民出版社"，<a href='/stark/app01/book/2/change/'>编辑</a>]]

        return new_data_list

    def get_list_filter_links(self):

        print(self.config_obj.list_filter)  # ['publish', 'authors']

        list_filter_links = {}

        for field in self.config_obj.list_filter:
            params = copy.deepcopy(self.request.GET)  # 不能放在循环外面

            current_filed_pk = params.get(field, 0)
            field_obj = self.config_obj.model._meta.get_field(field)
            from django.db.models.fields.related import ForeignKey, ManyToManyField

            if isinstance(field_obj, ForeignKey) or isinstance(field_obj, ManyToManyField):
                rel_model = field_obj.remote_field.model
                _limit_choices_to = field_obj.remote_field.limit_choices_to

                rel_model_queryset = rel_model.objects.filter(
                    **_limit_choices_to)  # [<Publish: 南京出版社>, <Publish: CCC>, <Publish: 海南出版社>]
                data_list = rel_model_queryset
            else:
                rel_model_queryset = []
                data_list = field_obj.choices

            temp = []
            # 处理 全部标签
            if params.get(field):
                del params[field]
                temp.append("<a class='btn btn-default btn-sm' href='?%s'>全部</a>" % params.urlencode())
            else:
                temp.append("<a  class='btn btn-default btn-sm active' href='#'>全部</a>")

            for obj in data_list:
                if type(obj) == tuple:
                    pk, text = obj[0], obj[1]
                else:
                    pk, text = obj.pk, str(obj)

                params[field] = pk

                if str(pk) == current_filed_pk:
                    link = "<a class='btn btn-default btn-sm active' href='?%s'>%s</a>" % (params.urlencode(), text)
                else:
                    link = "<a class='btn btn-default btn-sm' href='?%s'>%s</a>" % (params.urlencode(), text)
                temp.append(link)
            print("field_obj.verbose_name", field_obj.verbose_name)
            list_filter_links[field] = [field_obj.verbose_name, temp]

        return list_filter_links


class ModelStark(object):
    """
    默认配置类
    """
    list_display = ["__str__"]
    model_form_class = []
    list_display_links = []
    search_fields = []
    list_filter = []

    actions = []

    def __init__(self, model):
        self.model = model

        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label

    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.desc = "批量删除"

    # 反向解析当前查看表的增删改查的url
    def get_list_url(self):
        url_name = "%s_%s_list" % (self.app_label, self.model_name)
        _url = reverse(url_name)
        return _url

    def get_add_url(self):
        url_name = "%s_%s_add" % (self.app_label, self.model_name)
        _url = reverse(url_name)
        return _url

    def get_change_url(self, obj):
        url_name = "%s_%s_change" % (self.app_label, self.model_name)
        _url = reverse(url_name, args=(obj.pk,))
        return _url

    def get_del_url(self, obj):
        url_name = "%s_%s_delete" % (self.app_label, self.model_name)
        _url = reverse(url_name, args=(obj.pk,))
        return _url

    # 默认操作函数

    def edit(self, obj=None, is_header=False):
        if is_header:
            return "编辑"
        else:
            return mark_safe(
                "<a href='%s'><i class='fa fa-edit' aria-hidden='true'></i></a>" % self.get_change_url(obj))

    def delete(self, obj=None, is_header=False):
        if is_header:
            return "删除"
        return mark_safe("<a href='%s'><i class='fa fa-trash-o fa-lg'></i></a>" % self.get_del_url(obj))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return mark_safe("<input type='checkbox' id='choose'>")
        return mark_safe("<input type='checkbox' name='pk_list' value=%s>" % obj.pk)

    # 视图函数

    def new_list_display(self):
        temp = []
        temp.extend(self.list_display)

        temp.insert(0, ModelStark.checkbox)
        if not self.list_display_links:
            temp.append(ModelStark.edit)
        temp.append(ModelStark.delete)

        return temp

    def get_search_condition(self, request):

        val = request.GET.get("q")
        search_field = request.GET.get("search_field")
        search_condition = Q()
        if val:
            search_condition.children.append((search_field + "__icontains", val))

        return search_condition

    def get_filter_condition(self, request):
        filter_condition = Q()

        for key, val in request.GET.items():
            if key in ["page", "q", "search_field"]:
                continue
            filter_condition.children.append((key, val))

        return filter_condition

    def listview(self, request):

        """
        print(self) # 当前访问模型表的配置类对象
        print(self.model) # 当前访问模型表
        print("list_display:",self.list_display)  # ["title","price"]


        """

        if request.method == "POST":
            pk_list = request.POST.getlist("pk_list")

            queryset = self.model.objects.filter(pk__in=pk_list)
            action = request.POST.get("action")
            if action:
                action = getattr(self, action)
                action(request, queryset)

        add_url = self.get_add_url()
        data_list = self.model.objects.all()
        current_model_name = self.model._meta.verbose_name
        # 获取搜索条件对象
        search_condition = self.get_search_condition(request)
        # 获取filter的condition
        filter_condition = self.get_filter_condition(request)
        # 数据过滤

        data_list = data_list.filter(search_condition).filter(filter_condition)
        # 分页展示
        showlist = ShowList(self, data_list, request)
        print(showlist.get_list_filter_links())

        return render(request, "stark/list_view.html", locals())

    def get_new_form(self, form):
        from django.forms.boundfield import BoundField
        from django.forms.models import ModelChoiceField
        for bfield in form:

            if isinstance(bfield.field, ModelChoiceField):
                print(">>>", type(bfield.field))
                bfield.is_pop = True
                # 字段字符串
                print(bfield.name)

                rel_model = self.model._meta.get_field(bfield.name).remote_field.model
                model_name = rel_model._meta.model_name
                app_label = rel_model._meta.app_label
                if app_label == "auth": continue
                _url = reverse("%s_%s_add" % (app_label, model_name))
                bfield.url = _url
                bfield.pop_back_id = "id_" + bfield.name

        return form

    def get_model_form(self):

        if self.model_form_class:
            return self.model_form_class
        else:
            from django.forms import widgets as wid
            class ModelFormClass(forms.ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"

            return ModelFormClass

    def addview(self, request):
        current_model_name = self.model._meta.verbose_name
        ModelFormClass = self.get_model_form()

        if request.method == "POST":

            form = ModelFormClass(request.POST)
            form = self.get_new_form(form)
            if form.is_valid():
                obj = form.save()
                is_pop = request.GET.get("pop")
                if is_pop:
                    text = str(obj)
                    pk = obj.pk

                    return render(request, "stark/pop.html", locals())
                else:

                    return redirect(self.get_list_url())
            print("------>", form.errors)
            return render(request, "stark/add_view.html", locals())

        form = ModelFormClass()
        # form=self.get_new_form(form)

        return render(request, "stark/add_view.html", locals())

    def changeview(self, request, id):
        current_model_name = self.model._meta.verbose_name
        ModelFormClass = self.get_model_form()
        edit_obj = self.model.objects.get(pk=id)

        if request.method == "POST":
            form = ModelFormClass(data=request.POST, instance=edit_obj)
            form = self.get_new_form(form)
            if form.is_valid():
                form.save()  # update
                return redirect(self.get_list_url())

            return render(request, "stark/change_view.html", locals())

        form = ModelFormClass(instance=edit_obj)
        form = self.get_new_form(form)
        return render(request, "stark/change_view.html", locals())

    def delview(self, request, id):

        if request.method == "POST":
            self.model.objects.filter(pk=id).delete()
            return redirect(self.get_list_url())

        list_url = self.get_list_url()
        return render(request, "stark/del_view.html", locals())

    def extra_url(self):

        return []

    # 设计url
    def get_urls(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        temp = [

            url(r"^$", self.listview, name="%s_%s_list" % (app_label, model_name)),
            url(r"add/", self.addview, name="%s_%s_add" % (app_label, model_name)),
            url(r"(\d+)/change/", self.changeview, name="%s_%s_change" % (app_label, model_name)),
            url(r"(\d+)/delete/", self.delview, name="%s_%s_delete" % (app_label, model_name)),

        ]

        temp.extend(self.extra_url())

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class AdminSite(object):
    """
    stark组件的全局类
    """

    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class=None):
        # 设置配置类
        if not admin_class:
            admin_class = ModelStark

        self._registry[model] = admin_class(model)

    def get_urls(self):
        temp = []

        # print("admin----->",admin.site._registry)

        for model, config_obj in self._registry.items():
            print("model", model)  # Book
            print("config_obj", config_obj)  # BookConfig(Book)
            model_name = model._meta.model_name  # "book"
            app_label = model._meta.app_label  # "app01"

            temp.append(url(r"%s/%s/" % (app_label, model_name), config_obj.urls))

            '''
            temp=[
            
        
                #(1) url(r"app01/book/",BookConfig(Book).urls)
                #(2) url(r"app01/book/",(BookConfig(Book).get_urls(), None, None))
                #(3) url(r"app01/book/",([
                                                url(r"^$", BookConfig(Book).listview),
                                                url(r"add/$", BookConfig(Book).addview),
                                                url(r"(\d+)/change/$", BookConfig(Book).changeview),
                                                url(r"(\d+)/delete/$", BookConfig(Book).delview),
                                         ], None, None))
                                         
                ###########
                                         
                # url(r"app01/publish/",([
                                                url(r"^$", ModelStark(Publish).listview),
                                                url(r"add/$",  ModelStark(Publish).addview),
                                                url(r"(\d+)/change/$",  ModelStark(Publish).changeview),
                                                url(r"(\d+)/delete/$",  ModelStark(Publish).delview),
                                         ], None, None))
                                         
                                        
            
            ]
            
            
        
            '''

        return temp

    @property
    def urls(self):

        return self.get_urls(), None, None


site = AdminSite()
