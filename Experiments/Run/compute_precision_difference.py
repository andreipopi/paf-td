import os

def parse_results(file_path):
    results = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            instance_name = parts[0].split('.lp')[0]
            result_section = parts[2].strip()
            if "RESULT" in result_section:
                result_value = float(result_section.split()[1])
                results[instance_name] = f"{result_value:.15f}"
            else:
                results[instance_name] = "TIMEOUT"
    return results

def extract_system_name(file_path):
    return os.path.basename(file_path).split('_results.txt')[0]

def compare_results(file1, file2, output_file):
    results1 = parse_results(file1)
  
    results2 = parse_results(file2)
    system_name1 = extract_system_name(file1)
    system_name2 = extract_system_name(file2)
    
    max_instance_len = max(len(instance) for instance in results1.keys())
    max_system_name_len = max(len(system_name1), len(system_name2))
    max_result_len = max(max(len(result) for result in results1.values()), max(len(result) for result in results2.values()))
    
    print("max instance len", max_instance_len)

    print("max_system_name_len", max_system_name_len)


    count_differences = 0
    count_solved_by_both = 0
    count_percentage_above = 0
    with open(output_file, 'w') as f:
        header = f"{'Instance Name'.ljust(max_instance_len)},{'Result '.ljust(max_system_name_len)},{system_name1.ljust(max_system_name_len)},{system_name2.ljust(max_system_name_len)},Difference in Results\n"
        f.write(header)
        for instance, result1 in results1.items():
            result2 = results2.get(instance, "TIMEOUT")  # Default to TIMEOUT if instance is not in results2
            if result1 == "TIMEOUT" or result2 == "TIMEOUT":
                difference = "N/A - TIMEOUT"
                percentage_diff = "N/A - TIMEOUT"
            else:
                count_solved_by_both +=1
                difference = abs(float(result1) - float(result2))
                if difference > 1e-15:
                    count_differences += 1
                # Calculate percentage difference based on result1
                percentage_diff = (difference / float(result1)) * 100 if float(result1) != 0 else 0
                if percentage_diff > float(10):
                    count_percentage_above += 1
                difference = f"{difference:.15f}"
                percentage_diff = f"{percentage_diff:.2f}%"
                
            line = f"{instance.ljust(max_instance_len)},{result1.ljust(max_result_len)},{result2.ljust(max_result_len)},{difference},{percentage_diff}\n"
            f.write(line)


            
    
    return count_differences, count_solved_by_both, count_percentage_above

# Example usage
file_rational = "/Users/andrei/Documents/GitLab/praaf-tree-decomposition/Experiments/Run/compiled_results/td-python-ver-rational-efficient-join/td-python-ver-rational-efficient-join_results.txt"
file_real = "/Users/andrei/Documents/GitLab/praaf-tree-decomposition/Experiments/Run/compiled_results/td-python-ver-real-efficient-join/td-python-ver-real-efficient-join_results.txt"
output_comparison_file = "/Users/andrei/Documents/GitLab/praaf-tree-decomposition/Experiments/Run/comparison_precision.txt"


difference_count, count_solved_by_both, count_percentage_above = compare_results(file_rational, file_real, output_comparison_file)
print(f"Number of instances with differences in results up to 15 decimal places: {difference_count}")

print("number instances solved by both: ",count_solved_by_both )
print("number precision difference above 10%: ", count_percentage_above)