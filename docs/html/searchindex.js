Search.setIndex({docnames:["classifier","cli","data","events","index","misc","models","pipeline"],envversion:52,filenames:["classifier.rst","cli.rst","data.rst","events.rst","index.rst","misc.rst","models.rst","pipeline.rst"],objects:{"ramutils.classifier":{cross_validation:[0,0,0,"-"],model:[0,0,0,"-"],utils:[0,0,0,"-"]},"ramutils.classifier.cross_validation":{perform_cross_validation:[0,1,1,""],permuted_lolo_AUCs:[0,1,1,""],permuted_loso_AUCs:[0,1,1,""],run_lolo_xval:[0,1,1,""],run_loso_xval:[0,1,1,""]},"ramutils.classifier.model":{ModelOutput:[0,2,1,""]},"ramutils.classifier.model.ModelOutput":{compute_metrics:[0,3,1,""],compute_roc:[0,3,1,""],compute_tercile_stats:[0,3,1,""]},"ramutils.classifier.utils":{reload_classifier:[0,1,1,""],train_classifier:[0,1,1,""]},"ramutils.events":{clean_events:[3,1,1,""],coerce_study_pair_to_word_event:[3,1,1,""],combine_retrieval_events:[3,1,1,""],concatenate_events_across_experiments:[3,1,1,""],concatenate_events_for_single_experiment:[3,1,1,""],extract_sample_rate:[3,1,1,""],find_free_time_periods:[3,1,1,""],get_all_retrieval_events_mask:[3,1,1,""],get_baseline_retrieval_mask:[3,1,1,""],get_encoding_mask:[3,1,1,""],get_fr_retrieval_events_mask:[3,1,1,""],get_pal_retrieval_events_mask:[3,1,1,""],get_time_between_events:[3,1,1,""],get_vocalization_mask:[3,1,1,""],initialize_empty_event_reccarray:[3,1,1,""],insert_baseline_retrieval_events:[3,1,1,""],load_events:[3,1,1,""],normalize_pal_events:[3,1,1,""],partition_events:[3,1,1,""],preprocess_events:[3,1,1,""],remove_bad_events:[3,1,1,""],remove_incomplete_lists:[3,1,1,""],remove_intrusions:[3,1,1,""],remove_negative_offsets:[3,1,1,""],remove_nonresponses:[3,1,1,""],remove_practice_lists:[3,1,1,""],rename_correct_to_recalled:[3,1,1,""],select_all_retrieval_events:[3,1,1,""],select_baseline_retrieval_events:[3,1,1,""],select_encoding_events:[3,1,1,""],select_retrieval_events:[3,1,1,""],select_vocalization_events:[3,1,1,""],select_word_events:[3,1,1,""],subset_pal_events:[3,1,1,""],update_pal_retrieval_events:[3,1,1,""],update_recall_outcome_for_retrieval_events:[3,1,1,""]},"ramutils.exc":{MultistimNotAllowedException:[5,4,1,""],TooManyExperimentsError:[5,4,1,""],TooManySessionsError:[5,4,1,""],UnsupportedExperimentError:[5,4,1,""]},"ramutils.log":{get_logger:[5,1,1,""]},"ramutils.models":{hmm:[6,0,0,"-"]},"ramutils.models.hmm":{HierarchicalModel:[6,2,1,""],HierarchicalModelPlots:[6,2,1,""]},"ramutils.models.hmm.HierarchicalModel":{fit:[6,3,1,""]},"ramutils.models.hmm.HierarchicalModelPlots":{forestplot:[6,3,1,""],traceplot:[6,3,1,""]},"ramutils.parameters":{ExperimentParameters:[2,2,1,""],FRParameters:[2,2,1,""],FilePaths:[2,2,1,""],PALParameters:[2,2,1,""],StimParameters:[2,2,1,""]},"ramutils.schema":{Schema:[2,2,1,""]},"ramutils.schema.Schema":{from_hdf:[2,5,1,""],from_json:[2,5,1,""],to_dict:[2,3,1,""],to_hdf:[2,3,1,""],to_json:[2,3,1,""]},"ramutils.tasks":{classifier:[7,0,0,"-"],events:[7,0,0,"-"],make_task:[7,1,1,""],misc:[7,0,0,"-"],montage:[7,0,0,"-"],odin:[7,0,0,"-"],powers:[7,0,0,"-"],summary:[7,0,0,"-"],task:[7,1,1,""]},"ramutils.tasks.classifier":{serialize_classifier:[7,1,1,""]},"ramutils.tasks.misc":{read_index:[7,1,1,""]},"ramutils.tasks.montage":{extract_pairs_dict:[7,1,1,""],generate_pairs_for_classifier:[7,1,1,""],get_used_pair_mask:[7,1,1,""],load_pairs_from_json:[7,1,1,""],reduce_pairs:[7,1,1,""]},"ramutils.tasks.odin":{generate_pairs_from_electrode_config:[7,1,1,""],generate_ramulator_config:[7,1,1,""]},"ramutils.tasks.powers":{compute_normalized_powers:[7,1,1,""]},"ramutils.tasks.summary":{summarize_session:[7,1,1,""]},"ramutils.utils":{combine_tag_names:[5,1,1,""],extract_subject_montage:[5,1,1,""],reindent_json:[5,1,1,""],safe_divide:[5,1,1,""],sanitize_comma_sep_list:[5,1,1,""],save_array_to_hdf5:[5,1,1,""],timer:[5,1,1,""],touch:[5,1,1,""]},ramutils:{constants:[5,0,0,"-"],events:[3,0,0,"-"],exc:[5,0,0,"-"],log:[5,0,0,"-"],parameters:[2,0,0,"-"],utils:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","exception","Python exception"],"5":["py","classmethod","Python class method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:exception","5":"py:classmethod"},terms:{"boolean":[0,3],"case":7,"catch":[3,5],"class":[0,3,4,6],"default":[0,2,3,5,7],"float":[0,5],"function":[0,2,3,7],"import":[2,7],"int":[0,3,5,7],"new":[3,4],"return":[0,2,3,5,6,7],"true":[3,7],"try":[3,5],"while":7,ENS:7,For:[1,3],The:[3,7],There:[3,7],These:[0,3,7],Used:7,Useful:5,Uses:3,abil:7,about:2,absolut:[1,2,7],accept:7,account:1,across:3,activ:4,actual:[0,3],add:2,added:3,adding:7,affect:7,after:3,ahead:3,all:[0,1,2,3,4,5,7],all_pair:7,allow:7,alreadi:3,also:3,although:7,alwai:1,amount:3,amplitud:1,amplitudedetermin:1,analyz:3,ani:3,anod:[1,5],appli:[2,7],aren:0,arg:[5,7],argument:[0,1,2,5,7],around:2,arrai:[0,2,3,5,7],array_lik:[0,7],arug:7,associ:[2,7],assum:[3,7],attempt:5,attribut:[0,2],auc:0,automat:[3,4],avoid:3,backend:6,base:[2,3,6,7],baselin:3,basi:3,basic:3,bask:3,been:3,befor:3,begin:3,being:3,below:7,better:3,between:3,bin:7,bipolar:7,block:5,bool:[3,7],both:[0,3],bound:3,bptool:4,buffer:7,built:7,cach:[1,7],cachedir:1,calcul:[3,7],call:[0,3,7],callabl:7,can:[1,2,3,5,7],catfr3:1,catfr5:1,catfr6:1,catfr:3,cathod:[1,5],chang:7,channel:2,channel_1:7,check:3,classif:2,classifi:[2,3,4],classifier_contain:0,classifiercontain:[0,7],classififercontain:7,classiflib:[0,4],classmethod:2,clean:[3,5],clean_ev:3,clear:1,clone:4,code:[3,5],coerc:3,coerce_study_pair_to_word_ev:3,collect:[0,3],com:4,combin:3,combine_ev:3,combine_retrieval_ev:3,combine_tag_nam:5,come:7,comma:5,command:[4,5],common:[2,4,7],comparison:3,comput:0,compute_metr:0,compute_normalized_pow:7,compute_pow:7,compute_roc:0,compute_tercile_stat:0,concaten:3,concatenate_events_across_experi:3,concatenate_events_for_single_experi:3,conceiv:2,conda:4,conf:1,config:[1,3,7],configur:[2,4,5,7],consid:[2,3],contact:[5,7],contain:[0,3,5,6,7],context:5,convert:2,correct:[3,7],could:[2,5],crash:5,creat:[3,4,7],creation:[2,3],cross:[3,4,7],cross_valid:0,csv:[1,2,7],current:[3,7],curv:0,custom:[2,6],dask:7,data:[3,4,5,6,7],data_nam:5,dataset:[3,5],datatyp:3,debug:5,decor:7,defin:[4,5],delai:7,denomin:5,deseri:2,design:3,desir:3,dest:[1,2],destin:7,detail:[0,3],determin:3,dict:[0,7],dict_lik:0,dictionari:[2,5,7],differ:[1,3,7],dir:1,directori:[1,2,7],disk:3,displai:5,divis:5,doc:3,document:7,doe:7,doesn:5,done:[3,7],draw:[3,6],due:1,durat:3,dure:[0,7],each:[0,3,7],easili:[2,3],eeg:3,eegoffset:3,effect:4,elaps:5,electrod:[1,2,7],electrode_config_fil:[1,2],element:5,els:[4,7],empti:3,encod:[2,3,7],encoding_onli:3,end:[3,7],end_tim:3,enough:3,ensur:[2,7],env:4,environ:4,epoch:3,epoch_arrai:3,error:5,estim:[6,7],etc:[0,3],event:[0,4,5],event_list:3,everi:3,everyth:4,exc:5,except:[1,4],exclud:[3,7],excluded_pair:[2,7],exist:3,exit:1,experi:[1,2,3,5,6,7],experiment:4,experimentparamet:[2,7],extra:[0,3],extract:[3,5,7],extract_pairs_dict:7,extract_sample_r:3,extract_subject_montag:5,extran:5,failur:3,fals:[3,5,7],featur:[0,7],few:2,field:3,file:[1,2,3,4,5,7],filenam:2,filepath:[2,7],filesystem:1,filter:3,find:3,find_free_time_period:3,first:0,fit:[0,6],fixm:7,flag:3,flatten:3,follow:3,forc:1,forestplot:6,format:[2,5,7],former:7,found:[3,7],fr3:1,fr5:[0,1,7],fr6:[0,1],free:[2,3],frequenc:1,frequent:2,from:[0,2,3,5,6,7],from_hdf:2,from_json:2,frparamet:2,fuction:2,full:[3,7],func:7,futur:[3,4],gener:[3,4,5,6,7],generate_pairs_for_classifi:7,generate_pairs_from_electrode_config:7,generate_ramulator_config:7,get:[2,7],get_all_retrieval_events_mask:3,get_baseline_retrieval_mask:3,get_encoding_mask:3,get_fr_retrieval_events_mask:3,get_logg:5,get_pal_retrieval_events_mask:3,get_sample_weight:0,get_time_between_ev:3,get_used_pair_mask:7,get_vocalization_mask:3,git:4,github:4,given:[2,3,6],goe:7,graph:1,group:3,handl:2,happen:3,hardwar:7,have:[1,3],hdf5:[2,5],help:1,helper:3,here:[3,5],hierarch:6,hierarchicalmodel:6,hierarchicalmodelplot:6,high:3,hmm:6,homogen:3,how:3,http:4,identifi:[3,5,7],includ:[3,5,7],incomplet:3,incorpor:3,indent:5,independ:7,index:7,indic:3,infer:7,inform:5,inherti:2,initialize_empty_event_reccarrai:3,input_list:5,insert:3,insert_baseline_ev:3,insert_baseline_retrieval_ev:3,instanc:2,instead:[2,3],intrus:3,issu:1,item:3,item_comparison:6,iter:[0,3],joblib:7,json:[2,5,7],json_fil:5,jsonindexread:7,just:7,keyword:[0,2,7],know:2,kwarg:[0,2,7],kwd:5,label:1,latter:7,least:3,leav:0,leftov:5,length:3,level:3,liblinear:0,like:[5,7],line:4,list:[0,3,5,6,7],load:[0,3,7],load_ev:3,load_pairs_from_json:7,local:1,log:[1,4,7],log_arg:7,logger:5,logist:0,logisticregress:0,lolo:0,look:[3,7],lose:2,loso:0,maco:1,mai:[3,5],make:[3,7],make_task:7,manag:5,mani:[2,5],manner:2,manual:3,mark:3,mask:[3,7],match:3,matrix:[0,7],max:1,max_amplitud:1,maximum:1,mean:0,medtron:7,memori:3,mere:3,messag:[1,5],meta:7,method:[2,3],metric:7,mimic:5,min:1,min_amplitud:1,minim:7,minimum:1,minu:7,mirror:3,misc:7,miscellan:4,mode:[2,7],model:[0,2,4,7],modeloutput:[0,7],modifi:3,montag:[1,5],more:[0,2,3,7],mount:[0,1,2],mount_point:[0,7],multipl:5,multistimnotallowedexcept:5,multitrac:6,must:[0,3,7],n_permut:0,name:[3,5],natur:3,ndarrai:[0,3,5,7],necessari:3,need:[2,3,7],neg:3,neurorad:7,next:3,non:3,none:[3,7],normal:[3,7],normalize_pal_ev:3,note:[2,3,5,7],noth:3,nout:7,number:[0,1,3,5,7],numer:5,numpi:[2,3],object:[0,2,5,6,7],odin:[1,2],offset:3,one:[0,7],onli:[3,7],onset:3,oper:3,option:[0,1,7],order:[0,5],other:[3,7],out:[0,3],outcom:[0,3],output:[0,1,5],outstand:3,overrid:3,overwrit:5,packag:[2,4,5,7],pair:[2,7],pal1:0,pal3:1,pal5:[1,3],pal:[3,7],palparamet:2,parallel:7,param:7,paramet:[0,3,4,5,7],part:3,partial:7,particular:0,partit:3,partition_ev:3,pass:[0,2,5,7],path:[1,2,3,5,7],peform:3,penalti:0,penalty_param:0,penalty_typ:0,pennmem:4,percent:5,perform:[0,3,5],perform_cross_valid:0,period:3,permut:0,permuted_lolo_auc:0,permuted_loso_auc:0,pip:4,pipelin:4,pleas:2,plot:[5,6],plu:7,point:[0,2],possibl:[2,3,7],post:[3,7],pow_mat:0,power:0,practic:3,pre:3,precis:2,predefin:7,predict:0,preprocess_ev:3,prerequisit:4,preserv:5,prevent:5,primarili:[5,7],prior:7,prob:0,probabl:0,process:[4,5,7],product:1,proper:7,ps4:3,ps4_catfr5:1,ps4_fr5:1,ptsa:3,puls:1,pulse_frequ:1,purpos:5,pymc3:6,python:4,rais:[0,5,7],ram_clin:1,ram_util:4,ramul:[0,4],ramutil:[0,2,3,5,6,7],random:3,raw:[3,7],read:[3,7],read_index:7,reader:7,rec_bas:3,recal:[0,2,3],recarrai:[0,3,7],reccarrai:3,record:3,reduc:7,reduce_pair:7,redund:7,refer:4,regress:0,regular:0,reindent:5,reindent_json:5,rel:[1,2,3,7],relat:7,relev:2,reload_classifi:0,remain:4,remov:[3,5,7],remove_bad_ev:3,remove_incomplete_list:3,remove_intrus:3,remove_negative_offset:3,remove_nonrespons:3,remove_practice_list:3,rename_correct_to_recal:3,report:[3,5],repositori:4,repres:7,request:3,requir:[3,4],rerun:1,respons:3,result:[0,3,5,7],resum:7,retriev:[3,7],return_exclud:7,rhino:[0,1,2],roc:0,root:[1,2,3,7],rootdir:3,run:[1,6,7],run_lolo_xv:0,run_loso_xv:0,runtimeerror:[0,7],safe_divid:5,same:[2,3,7],sampl:6,sample_weight:[0,7],sampler:3,sanitize_comma_sep_list:5,save:[1,2,5],save_array_to_hdf5:5,schema:2,score:0,script:1,search:7,second:3,see:[0,3],select:3,select_all_retrieval_ev:3,select_baseline_retrieval_ev:3,select_encoding_ev:3,select_retrieval_ev:3,select_vocalization_ev:3,select_word_ev:3,sens:3,sensibl:5,separ:5,seri:7,serial:[2,7],serializ:4,serialize_classifi:7,serv:3,session:[0,3,5,7],sessionsummari:7,set:[0,3,7],setup:4,shorthand:0,should:[3,4],show:1,simpli:7,sinc:[3,7],singl:[0,2,3,7],site:5,skip:3,sklearn:[0,7],smatter:3,solver:0,some:[2,7],someth:[5,7],sort:7,sourc:[0,2,3,4,5,6,7],span:7,specif:[3,7],specifi:7,split:3,sshf:1,standard:[3,7],start:[3,7],start_tim:3,stat:0,statist:0,step:3,stim:[1,4,5,7],stim_param:7,stimparamet:[2,7],stimul:[2,7],store:[0,7],str:[0,2,3,5,7],string:[2,5],structur:[3,4,7],study_pair:3,subclass:2,subject:[0,1,3,5,6,7],subject_id:5,subset:[3,7],subset_pal_ev:3,success:3,summar:7,summarize_sess:7,suppli:7,support:5,surrog:3,tag_name_list:5,taken:3,target:1,target_amplitud:1,task:[0,1,2,3,4],templat:[5,7],tercil:0,test_env:4,than:7,them:3,thi:[1,2,3,7],those:[3,7],throughout:5,time:[0,2,3,5,7],timer:5,titl:6,to_dict:2,to_hdf:2,to_json:2,too:5,toomanyexperimentserror:5,toomanysessionserror:[5,7],touch:5,trace:6,traceplot:6,train:[2,3,4,7],train_classifi:0,trait:2,treat:1,trial:[0,3],trivial:3,true_label:0,tune:6,tupl:5,two:3,type:[0,2,3,4,6,7],underli:5,unifi:1,uniqu:3,unix:5,unsupportedexperimenterror:5,updat:3,update_pal_retrieval_ev:3,update_recall_outcome_for_retrieval_ev:3,usag:4,use:[0,1,2,5,7],used:[0,2,3,5,7],useful:[2,5],user:7,uses:2,using:[2,6,7],usual:0,util:[3,4],valid:[3,4,7],valu:[0,2,3,5,7],vector:0,verifi:7,via:[1,7],visibl:2,vispath:1,visual:1,vocal:3,wai:3,want:2,weight:7,were:3,what:3,when:[0,2,3,5,7],whenev:2,wherev:3,whether:[3,7],which:[2,3,5,7],whitespac:5,whose:3,width:5,window:2,within:3,without:3,word:3,work:7,worth:5,would:3,wrap:7,write:[1,2],wrong:7,xval:0,xval_output:7,yet:[0,5],yml:4,you:[2,3],zero:5,zip:7},titles:["Classifier training, cross validation, and utilities","Command-line usage","Serializable data structures","Event processing","ramutils","Miscellaneous utilities","Modeling effects of stim","Pipelines"],titleterms:{"class":2,"function":5,classifi:[0,7],command:1,common:5,comput:7,configur:1,constant:5,content:4,cross:0,data:2,defin:[2,7],effect:6,els:5,event:[3,7],everyth:5,except:5,experiment:2,gener:1,instal:4,line:1,log:5,miscellan:[5,7],model:6,montag:7,odin:7,paramet:2,pipelin:7,power:7,process:3,ramul:[1,7],ramutil:4,refer:[0,7],report:7,serializ:2,stim:6,structur:2,summari:7,task:7,train:0,type:5,usag:1,util:[0,5],valid:0}})