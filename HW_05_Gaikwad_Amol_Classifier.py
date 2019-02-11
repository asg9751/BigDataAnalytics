# Generated classifier file. Few indentations need to be corrected.
__author__ = 'Amol Gaikwad'
import pandas as pd
target_class = ["Cupcake", "Muffin"]

def tree(attr):
	if float(attr[3]) <19.55:
		if float(attr[5]) <12.5:
			if float(attr[4]) <19.0:
				if float(attr[6]) <3.0:
					return target_class[1]
				else:
					if float(attr[1]) <42.0:
						return target_class[1]
					else:
						return target_class[0]
					else:
						return target_class[0]
					else:
						return target_class[0]
					else:
						if float(attr[5]) <24.1:
							if float(attr[1]) <41.49:
								return target_class[0]
							else:
								if float(attr[1]) <42.0:
									return target_class[1]
								else:
									return target_class[0]
								else:
									return target_class[1]

    def main():
    csv_data = pd.read_csv("Recipes_For_VALIDATION_2181_RELEASED_v202.csv")
    len_data = len(csv_data)
    f = open("HW_05_Gaikwad_Amol_MyClassifications.csv", "w+")

    for x in range(0, len_data):
        res = tree(csv_data.iloc[x,1:])
        if res!=None:
            f.write(res)
            f.write()

    csv_data = pd.read_csv("Recipes_For_Release_2181_v202.csv")
    len_data = len(csv_data)
    # fp = open("HW_05_Gaikwad_Amol_Accuracy.csv", "w+")

    correct_hits = 0
    total = len_data
    for x in range(0, len_data):
        res = tree(csv_data.iloc[x, 1:])
        if res != None:
            if res == csv_data["Type"].tolist()[x]:
                correct_hits = correct_hits +1

    accuracy = (correct_hits / total) * 100
    print("Output of validation file generated in HW_05_Gaikwad_Amol_MyClassifications.csv file")
    print("Accuracy of training data is "+str(accuracy)+" percent")


if __name__ == '__main__':
    main()
    