  try:
    import traceback
    import sys
    from pypuppetdb import connect
    import pymssql
    import json
    from collections import OrderedDict
  except:
    print(traceback.format_exc())

  try:
    # import the required libs
    pdb = None
    node = None
    source = "PuppetDB"
    fqdn = None
    # Catch PuppetDB mistakes.
    try:
      pdb = connect()
      node = pdb.node('ryglif75.labdomain.net')
    except:
      print("Error connecting to PuppetDB")
      print(traceback.format_exc())
      sys.exit(3)
    try:
      msconn = pymssql.connect(server='10.13.37.17', database = 'test1', user='testuser', password='B17bombefly') 
      mscursor = msconn.cursor(as_dict=True)
    except:
      print("Error connecting to database")
      print(traceback.format_exc())
      sys.exit(3)
    mscursor.execute("SELECT config from utility_scripts where script like 'PuppetDB' and parameter like 'metafacts'")
    row = mscursor.fetchone()
    metafacts = row['config']
    #metafacts = ['path','uptime','uptime_seconds','uptime_days','uptime_hours','system_uptime','swapfree','swapfree_mb','memoryfree','memoryfree_mb','memory','mountpoints','load_averages',]
    metaresult = {}
    factresult = {}
    for fact in node.facts():
      if (fact.name in metafacts):
        metaresult[fact.name] = fact.value
      else:
        if (fact.name == 'fqdn'):
        fqdn = fact.value
        factresult[fact.name] = fact.value
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
    source_key = fqdn
    jsonblob =  json.dumps(factresult)
    metablob = json.dumps(metaresult)
    params = (source,source_key,source,source_key,jsonblob,metablob,jsonblob,source,source_key,jsonblob,metablob,source,source_key)
    query = """
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
    mscursor.execute (query,params)
    msconn.commit()
  except Exception as err:
    print(traceback.format_exc())
  finally:
    msconn.close()
