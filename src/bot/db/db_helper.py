

def members_to_dict(members,addType=False):
    mem_id = [mem.id for mem in members]
    mem_name = [mem.name for mem in members]
    if(addType):
        mem_type = [mem.type for mem in members]
        [print(mem.type) for mem in members]
        mem_dict = [{'id':id,'name':name,'type':str(_type)} for id,name,_type in zip(mem_id,mem_name,mem_type)]
    else:
        mem_dict = [{'id':id,'name':name} for id,name in zip(mem_id,mem_name)]
    return mem_dict