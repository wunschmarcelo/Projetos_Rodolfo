"""Generate a standard App Inventor/Kodular .aia project from local assets."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'project'
SRC = PROJECT / 'src/appinventor/ai_florescer/Florescer'
SRC.mkdir(parents=True, exist_ok=True)
# Conservative App Inventor component versions allow the importer to upgrade them.
form = {'authURL':['ai2.appinventor.mit.edu'], 'YaVersion':'208', 'Source':'Form', 'Properties':{
 '$Name':'Screen1','$Type':'Form','$Version':'26','Uuid':'0',
 'AppName':'Florescer','Title':'Florescer','TitleVisible':'False','ShowStatusBar':'True',
 'Sizing':'Responsive','Scrollable':'False','ScreenOrientation':'portrait',
 'BackgroundColor':'&HFFFFFCF4','PrimaryColor':'&HFFF4B721','PrimaryColorDark':'&HFFB88013',
 'AccentColor':'&HFFF4B721','Theme':'AppTheme.Light.DarkActionBar',
 '$Components':[
  {'$Name':'WebViewer1','$Type':'WebViewer','$Version':'8','Uuid':'1001','Width':'-2','Height':'-2','HomeUrl':'','FollowLinks':'True','IgnoreSslErrors':'False','PromptforPermission':'False'},
  {'$Name':'ActivityStarter1','$Type':'ActivityStarter','$Version':'6','Uuid':'1002','Action':'android.intent.action.DIAL'},
  {'$Name':'Notifier1','$Type':'Notifier','$Version':'4','Uuid':'1003'}]}}
(SRC/'Screen1.scm').write_text('#|\n$JSON\n'+json.dumps(form,ensure_ascii=False,separators=(',',':'))+'\n|#',encoding='utf-8')
xml=ET.Element('xml',{'xmlns':'http://www.w3.org/1999/xhtml'})
counter=0
def block(kind,parent=None,**attrs):
 global counter
 counter+=1
 return ET.SubElement(parent if parent is not None else xml,'block',{'type':kind,'id':'florescer_'+str(counter),**{k:str(v) for k,v in attrs.items()}})
def field(b,name,value): ET.SubElement(b,'field',{'name':name}).text=value

def text(parent,value):
 b=block('text',parent);field(b,'TEXT',value);return b

def event(component,typ,name,x,y):
 b=block('component_event',x=x,y=y);ET.SubElement(b,'mutation',{'component_type':typ,'is_generic':'false','instance_name':component,'event_name':name});field(b,'COMPONENT_SELECTOR',component);return ET.SubElement(b,'statement',{'name':'DO'})

def method(parent,component,typ,name,arg=None):
 b=block('component_method',parent);ET.SubElement(b,'mutation',{'component_type':typ,'method_name':name,'is_generic':'false','instance_name':component});field(b,'COMPONENT_SELECTOR',component)
 if arg is not None:text(ET.SubElement(b,'value',{'name':'ARG0'}),arg)
 return b

def prop(parent,component,typ,name,value):
 b=block('component_set_get',parent);ET.SubElement(b,'mutation',{'component_type':typ,'set_or_get':'set','property_name':name,'is_generic':'false','instance_name':component});field(b,'COMPONENT_SELECTOR',component);field(b,'PROP',name)
 v=ET.SubElement(b,'value',{'name':'VALUE'})
 if isinstance(value,str):text(v,value)
 else:value(v)
 return b

def get_webstring(parent):
 b=block('component_set_get',parent);ET.SubElement(b,'mutation',{'component_type':'WebViewer','set_or_get':'get','property_name':'WebViewString','is_generic':'false','instance_name':'WebViewer1'});field(b,'COMPONENT_SELECTOR','WebViewer1');field(b,'PROP','WebViewString')

def next_of(b):return ET.SubElement(b,'next')

init=event('Screen1','Form','Initialize',20,20)
method(init,'WebViewer1','WebViewer','GoToUrl','file:///android_asset/index.html')
changed=event('WebViewer1','WebViewer','WebViewStringChange',20,180)
choose=block('controls_if',changed);ET.SubElement(choose,'mutation',{'elseif':'1'})
# Allow exactly the two support numbers; never accept arbitrary bridge commands.
for i,number in enumerate(['188','192']):
 compare=block('logic_compare',ET.SubElement(choose,'value',{'name':'IF'+str(i)}));field(compare,'OP','EQ')
 get_webstring(ET.SubElement(compare,'value',{'name':'A'}));text(ET.SubElement(compare,'value',{'name':'B'}),'tel:'+number)
 body=ET.SubElement(choose,'statement',{'name':'DO'+str(i)})
 a=prop(body,'ActivityStarter1','ActivityStarter','DataUri','tel:'+number)
 method(next_of(a),'ActivityStarter1','ActivityStarter','StartActivity')
back=event('Screen1','Form','BackPressed',20,650)
method(back,'WebViewer1','WebViewer','RunJavaScript',"(() => {const d=document.querySelector('dialog[open]');if(d){d.close();return;}const tab=document.querySelector('[data-tab=checkin]');if(tab && !tab.classList.contains('active')){tab.click();return;}window.AppInventor.setWebViewString('confirm-exit');})()")
# Add a separate IF after the telephone dispatch to confirm exiting.
exit_if=block('controls_if',next_of(choose))
compare=block('logic_compare',ET.SubElement(exit_if,'value',{'name':'IF0'}));field(compare,'OP','EQ');get_webstring(ET.SubElement(compare,'value',{'name':'A'}));text(ET.SubElement(compare,'value',{'name':'B'}),'confirm-exit')
body=ET.SubElement(exit_if,'statement',{'name':'DO0'})
b=block('component_method',body);ET.SubElement(b,'mutation',{'component_type':'Notifier','method_name':'ShowChooseDialog','is_generic':'false','instance_name':'Notifier1'});field(b,'COMPONENT_SELECTOR','Notifier1')
for i,value in enumerate(['Deseja sair do Florescer? Seus registros salvos ficam neste aparelho.','Até logo 🌻','Sair','Continuar']):text(ET.SubElement(b,'value',{'name':'ARG'+str(i)}),value)
boolb=block('logic_boolean',ET.SubElement(b,'value',{'name':'ARG4'}));field(boolb,'BOOL','TRUE')
after=event('Notifier1','Notifier','AfterChoosing',20,920)
cond=block('controls_if',after);comp=block('logic_compare',ET.SubElement(cond,'value',{'name':'IF0'}));field(comp,'OP','EQ')
local=block('lexical_variable_get',ET.SubElement(comp,'value',{'name':'A'}));field(local,'VAR','get choice');text(ET.SubElement(comp,'value',{'name':'B'}),'Sair')
block('controls_closeApplication',ET.SubElement(cond,'statement',{'name':'DO0'}))
error=event('Screen1','Form','ErrorOccurred',650,20)
method(error,'Notifier1','Notifier','ShowAlert','Não foi possível concluir essa ação. Se o discador não estiver disponível, ligue 188 para apoio emocional ou 192 em uma emergência, usando outro telefone.')
ET.SubElement(xml,'yacodeblocks',{'ya-version':'208','language-version':'36'})
ET.indent(xml)
(SRC/'Screen1.bky').write_text(ET.tostring(xml,encoding='unicode'),encoding='utf-8')
properties='''main=appinventor.ai_florescer.Florescer.Screen1
name=Florescer
assets=../assets
source=../src
build=../build
versioncode=1
versionname=1.0
useslocation=False
aname=Florescer
sizing=Responsive
showlistsasjson=True
actionbar=False
theme=AppTheme.Light.DarkActionBar
color.primary=&HFFF4B721
color.primary.dark=&HFFB88013
color.accent=&HFFF4B721
'''
(PROJECT/'youngandroidproject').mkdir(exist_ok=True)
(PROJECT/'youngandroidproject/project.properties').write_text(properties,encoding='utf-8')
output=ROOT.parent/'entregas/Florescer.aia'
output.parent.mkdir(exist_ok=True)
with ZipFile(output,'w',ZIP_DEFLATED) as z:
 for f in sorted(PROJECT.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(PROJECT).as_posix())
 for f in sorted((ROOT/'assets').iterdir()):
  if f.is_file():z.write(f,'assets/'+f.name)
print(output)
