import os
import sys

walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

results_path = os.path.join(os.path.abspath(walk_dir), 'dump-results.txt')

interest_count = 0
interest_len = 0
data_count = 0
data_len = 0
total_len = 0

with open(results_path, 'wb') as output:
    for root, subdirs, files in os.walk(walk_dir):
        print('--\nroot = ' + root)

        for subdir in subdirs:
            print('\t- subdirectory ' + subdir)

        for filename in files:
            if "dump" in filename:
                file_path = os.path.join(root, filename)
                print('\t- file %s (full path: %s)' % (filename, file_path))
                with open(file_path, 'rb') as f:
                    lines = f.readlines()
                    for line in lines:
                        size = int(line.split(",")[2].split()[1])
                        if "INTEREST" in line:
                            interest_count += 1
                            interest_len += size
                        if "DATA" in line:
                            data_count += 1
                            data_len += size
                        total_len += size

    out_str = "Interest count="+str(interest_count)+ " size="+str(interest_len)+"\n"\
              + "Data count="+str(data_count)+" size="+str(data_len)+"\n"\
              + "Total size="+str(total_len)+"\n"
    print(out_str)
    output.write(out_str)


