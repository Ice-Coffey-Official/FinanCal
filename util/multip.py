'''from multiprocessing import Pool
from config import processors

def multiCoreRun(func, arg, processors=processors):
    with Pool(processes=processors) as pool:
        pool.map(func, arg)'''

"""from multiprocessing import Pool, freeze_support, current_process
from config import processors
from utilFun import append_to_json

def multiCoreRun(func, key, jsonDict, filename):

    with Pool(processes=processors) as pool:
        args = [(key, jsonDict, 'results/'+filename) for x in range(0,processors)] + [(key, jsonDict, 'results/'+filename) for x in range(0,processors)] + [(key, jsonDict, 'results/'+filename) for x in range(0,processors)]
        pool.starmap(func, args)

if __name__ == "__main__":
    freeze_support()
    multiCoreRun(append_to_json, 'city', {
                                    "sub_category_2_name": "General",
                                    "gross": "$4,939,596,246",
                                    "percent": "100.00%",
                                    "line_item": [
                                        {
                                            "line_item_name": "Administration_General",
                                            "gross": "$3,098,851,562",
                                            "percent": "62.73%"
                                        },
                                        {
                                            "line_item_name": "Aid Programs Cash_General",
                                            "gross": "$1,760,054,573",
                                            "percent": "35.63%"
                                        },
                                        {
                                            "line_item_name": "Other Welfare_General",
                                            "gross": "$80,690,111",
                                            "percent": "1.63%"
                                        }
                                    ]
                                }, 'data')
"""