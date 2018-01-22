import json

if __name__ == "__main__":
    json_file = open("config.json",'r')
    json_data = json.load(json_file)
    print json_data
    #for a in b:
    #   is enable
    #       restult = do_test
    #       console.log(name status restult)