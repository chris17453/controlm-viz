import sys
import untangle
from collections import OrderedDict 

from pprint import pprint

def load_xml(xml_file):
    #print ("Parsing: {0}".format(xml_file))
    with open(xml_file, 'r') as ds:
        data=ds.read()
    try:
        result_meta = untangle.parse(data)
    except Exception as err:
        sys.exit("There is an issue the xml stream:\n   {0}\n".format(err))
    
    #pprint(result_meta,indent=4)
    

    results=create_object(result_meta)
    create_class(results)
    #pprint(results)

#    package=map_xml.parse(result_meta,{})
    #namespaces=package['namespace']
    #return parsed_data


def create_object(xml_object):
    
    if xml_object==None:
        return None

    factory_obj={}
    _name=xml_object._name
    if xml_object._attributes:
        #factory_obj['attributes']={}
        for attr in xml_object._attributes:
            factory_obj[attr]=xml_object._attributes[attr]
            


    if xml_object.children:
        #factory_obj['children']=[]
        for child in xml_object.children:
            obj=create_object(child)
            if obj==None:
                continue

            if child._name in factory_obj:
                if isinstance(factory_obj[child._name],list)==True:
                    factory_obj[child._name].append(obj)
                else:
                    odd=factory_obj[child._name]
                    arr=[odd]
                    factory_obj[child._name]=arr
                    factory_obj[child._name].append(obj)
            
            else:
                factory_obj[child._name]=obj
    if xml_object.cdata:
        data=xml_object.cdata.strip()
        if len(data)>0:
            if len(factory_obj)==0:
                return data
            
            factory_obj['cdata']=data

    if len(factory_obj)==0: return None
    #factory_obj['name']=xml_object._name
    return factory_obj



def create_class(data,depth=0,uuid="root"):
    if depth==0:
        print("blockdiag {")
    padd=""
    #for i in range(0,depth):
    #    padd+=" "
    #print("{0} class {1}".format(padd,uuid) )
    if isinstance(data,dict):
        for node in data:
            uuid_node="{0}_{1}".format(uuid,node)
            #uuid_node="{0}".format(node)
            print("{0} -> {1}".format(uuid,uuid_node))
            create_class(data[node],depth+1,uuid=uuid_node)
        
    
    elif isinstance(data,list):
        index=0
        for node in data:
            
            uuid_node="{0}_{1}".format(uuid,index)
            #uuid_node="{0}[]".format(uuid)
            print("{0} -> {1}".format(uuid,uuid_node))
            create_class(node,depth+1,uuid=uuid_node)
            index+=1
    else:
        print("{0} -> \"{1}\"".format(uuid,data))
        pass
    
    if depth==0:
        print ("}")
    #pprint(data)


if __name__ == "__main__":
    file="data/jcl/pas_out_processing.jcl"
    
    load_xml(file)