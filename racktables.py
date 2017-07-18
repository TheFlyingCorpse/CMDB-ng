try:
  import traceback
  import sys
  import MySQLdb
  import pymssql
  import json
  from collections import OrderedDict
except:
  print(traceback.format_exc())

try:
  # import the required libs
  pdb = None
  node = None
  source = "RackTables"
  source_key = None
  # Catch MySQL mistakes.
  try:
    mydb = MySQLdb.connect(host='server1.labdomain.net',user='readonlyuser',passwd='ixa3HHdljNstSYyz',db='racktables')
    mycursor = mydb.cursor(MySQLdb.cursors.DictCursor)
  except:
    print("Error connecting to MySQLdb")
    print(traceback.format_exc())
    sys.exit(4)
  try:
    msconn = pymssql.connect(server='10.13.37.17', database = 'test1', user='testuser', password='B17bombefly') 
    mscursor = msconn.cursor(as_dict=True)
  except:
    print("Error connecting to database")
    print(traceback.format_exc())
    sys.exit(3)
  mscursor.execute("SELECT config from utility_scripts where script like 'RackTables' and parameter like 'metafacts'")
  row = mscursor.fetchone()
  metafacts = row['config']
  #metafacts = ['path','uptime','uptime_seconds','uptime_days','uptime_hours','system_uptime','swapfree','swapfree_mb','memoryfree','memoryfree_mb','memory','mountpoints','load_averages',]
  object_id = 24
  myparams = [object_id]
  myquery = """SET @object_id = %s;"""
  mycursor.execute(myquery,myparams)
  myquery = """
SELECT 'int' as type,'object_id' as rkey, @object_id as rvalue
UNION
SELECT 'dict' as type,'ObjectType' as rkey,d.dict_value as rvalue FROM Dictionary d, Object o, Chapter c
WHERE o.id = @object_id AND c.id=d.chapter_id AND c.name = 'ObjectType' AND d.dict_key=o.objtype_id
UNION
SELECT a.type,a.name as rkey,av.string_value as rvalue from Object o inner join AttributeValue av ON av.object_id=o.id join Attribute a ON a.id=av.attr_id LEFT OUTER join Dictionary d ON d.chapter_id=a.id 
WHERE o.id = @object_id AND a.type = 'string'
UNION
SELECT a.type,a.name as rkey,d.dict_value as rvalue from Dictionary d, Object o inner join AttributeValue av ON av.object_id=o.id join Attribute a ON a.id=av.attr_id
WHERE a.type = 'dict' and o.id = @object_id AND d.dict_key=av.uint_value
UNION
SELECT a.type,a.name as rkey,FROM_UNIXTIME(av.uint_value,'%Y-%m-%d') as rvalue from Object o inner join AttributeValue av ON av.object_id=o.id join Attribute a ON a.id=av.attr_id
WHERE a.type = 'date' and o.id = @object_id AND av.uint_value
UNION
SELECT a.type,a.name as rkey,av.float_value as rvalue from Object o inner join AttributeValue av ON av.object_id=o.id join Attribute a ON a.id=av.attr_id
WHERE a.type = 'float' and o.id = @object_id AND av.float_value
UNION
SELECT a.type,a.name as rkey,av.uint_value as rvalue from Object o inner join AttributeValue av ON av.object_id=o.id join Attribute a ON a.id=av.attr_id
WHERE a.type = 'uint' and o.id = @object_id AND av.uint_value"""
  mycursor.execute(myquery)
  facts = mycursor.fetchall()
  metaresult = {}
  factresult = {}
  for fact in facts:
    fact_name = fact['rkey']
    fact_value = fact['rvalue']
    print(fact_name)
    print(fact_value)
    if (fact_name in metafacts):
      metaresult[fact_name] = fact_value
    else:
      if (fact_name == 'object_id'):
        source_key = fact_value
      factresult[fact_name] = fact_value
  def sortOD(od):
    res = OrderedDict()
    for k, v in sorted(od.items()):
      if isinstance(v, dict):
        res[k] = sortOD(v)
      else:
        res[k] = v
    return res
  factresult = sortOD(factresult)
  metaresult = sortOD(metaresult)
 
  jsonblob =  json.dumps(factresult)
  if (metaresult):
    metablob = json.dumps(metaresult)
  else:
    metablob = None
  msparams = (source,source_key,source,source_key,jsonblob,metablob,jsonblob,source,source_key,jsonblob,metablob,source,source_key)
  msquery = """
  IF NOT EXISTS (SELECT source_key FROM dbo.ObjectStore WHERE source = %s AND source_key = %s)
    BEGIN
    INSERT INTO dbo.ObjectStore(source,source_key,jsonblob,metablob)
         VALUES (%s,%s,%s,%s);
    END
  ELSE
    BEGIN
    UPDATE dbo.ObjectStore SET jsonblob = %s, jsonlastmodified = GetDate() WHERE source = %s and source_key = %s and jsonblob <> %s
    UPDATE dbo.ObjectStore SET metablob = %s, metalastmodified = GetDate() WHERE source = %s and source_key = %s
    END
  """
  #   --IF NOT EXISTS (SELECT TOP(1) source_key FROM dbo.ObjectStore WHERE source = %s AND source_key = %s AND jsonblob = %s ORDER by id desc)
  mscursor.execute (msquery,msparams)
  msconn.commit()
except Exception as err:
  print(traceback.format_exc())
finally:
  msconn.close()
