from django.conf.urls import patterns, url


from iliasApp import views


urlpatterns = [

    url(r"^$", views.homeView, name="ViewHome"),

    url(r"^MPRA/$", views.indexView, name="ViewIndex"),
    url(r"^MPRAResults/$", views.resultsView, name="ViewResults"),

    url(r"^Transmutation/$", views.part3View, name="ViewPart3"),
    url(r"^TransmutationResults/$", views.part3RresultsView, name="ViewPart3Results"),

    url(r"^documentation/$", views.docsView, name="ViewDocs"),

    url(r"^MutationDownload/$", views.mutationDownloadView, name="ViewMutationDownload"),

    url(r"^MPRA/SNPs/$", views.mpraSnp, name="ViewMpraSnp"),
    url(r"^MPRAResults/SNPs/$", views.mpraSnpResults, name="ViewMpraSnpResults"),
    url(r"^ScriptDownload/(?P<fileToDownload>\w+)/$", views.downloadScriptView, name="ViewDownloadScript"),


    # apis
    url(r"^API/MPRA/SNP$", views.MpraSnpApiView, name="ViewMpraSnpApi"),


    url(r"^test/$", views.testView, name="ViewTest"),
    url(r"^", views.restView, name="ViewRest"),



]
