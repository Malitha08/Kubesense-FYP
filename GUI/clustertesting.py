from DatasetCreator import DatasetCreator
from MultiModelCommandGenerator import KubesenseGenerator
from driver import KubeDriver

file_path = 'C:/Users/acer/Desktop/(DS and AI) Lectures/4th Year/CM4605-Individual Research Project/kubesense/Kubesense-FYP/Kubesense/Dataset/updted_data_with_class.json'
creator = DatasetCreator(json_path=file_path, csv_path='data.csv')
data = creator.create_dataset()

kubesense_generator = KubesenseGenerator()
driver = KubeDriver(data, kubesense_generator)

user_input = "Can I view the namespaces available in the cluster"
# output = driver.generate(user_input)
# print("[SUCCESS] Output: ", output)


output_from_cluster = driver.generate_and_execute(user_input)
print("Output from cluster: ", output_from_cluster)


# user_input = "i want to get the namespaces available"
# a = "kubectl get namespaces"
# b = "kubectl get namespaces"
# x = kubesense_generator.custom_ensemble(user_input, a, b)
# print(x)