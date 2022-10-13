import glob
import argparse
import re
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='headers_directory', required=True)
    parser.add_argument('-o', dest='output_directory', required=True)
    args = parser.parse_args()

    # create full paths
    headers_path = Path().resolve() / args.headers_directory
    output_path = Path().resolve() / args.output_directory
    print('Headers path: {}'.format(headers_path))
    print('Output path: {}'.format(output_path))


    # find all topic json files
    header_files = glob.glob(f'{headers_path}/*.h')
    print('Found {} header files'.format(len(header_files)))

    # if files list is empty return error
    if not header_files:
        print('No files found')
        exit(1)

    # delete output directory if it exists
    if output_path.exists():
        shutil.rmtree(output_path)

    # create output directory with all parent directories
    output_path.mkdir(parents=True)

    # create inc and src directories
    inc_path = output_path / 'inc'
    src_path = output_path / 'src'
    inc_path.mkdir()
    src_path.mkdir()

    # open each header file
    for file in header_files:
        f = open(file)

        # scan c header file and look for all function prototypes using regex
        # examples: 
        # return_type function_name (type name, type name, ...);
        # void function_name (type name, type name, ...);
        # return_type function_name (void);
        # void function_name ();
        # void function_name (const char* name);

        # find all function prototypes
        function_prototypes = re.findall(r'([\w|*|" "]+)\s(\w+)\s*\(((\w|\s|[,]|[*]|\[|\])*)\);', f.read())

        # remove if contains 'typedef'
        function_prototypes = [x for x in function_prototypes if 'typedef' not in x[0]]

        print('Generating mocks for: ' + file)

        # extract return type, function name, and arguments from each function prototype using regex
        functions = []
        for function in function_prototypes:
            # extract return type
            return_type = function[0].strip()

            # extract function name
            function_name = function[1]

            # extract arguments
            arguments = function[2]
            # split arguments into list of tuples
            arguments = arguments.split(',')

            # extract argument types
            argument_types = []
            for argument in arguments:
                # if is 'void' or '', add 'void' to list
                if argument == 'void' or argument == '':
                    argument_types.append('void')
                else:
                    # split by whitespace and remove last element
                    argument_types.append(' '.join(argument.split()[:-1]))

            functions.append({'return_type': return_type, 'function_name': function_name, 'argument_types': argument_types})

        # create mock file .c and .h in inc and src
        mock_file_c = open(f'{output_path}/src/{Path(file).stem}_mock.c', 'w')
        mock_file_h = open(f'{output_path}/inc/{Path(file).stem}_mock.h', 'w')

        # write header to mock file .h
        mock_file_h.write('#pragma once\n')
        mock_file_h.write(f'#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))\n')
        mock_file_h.write(f'#include <{Path(file).name}>\n')
        mock_file_h.write(f'#include <fff.h>\n\n')
        # write mock function prototypes to mock file .h
        for function in functions:
            # if function returns void
            if function['return_type'] == 'void':
                # DECLARE_FAKE_VOID_FUNC(function_name)
                if function['argument_types'][0] == 'void':
                    mock_file_h.write(f'DECLARE_FAKE_VOID_FUNC({function["function_name"]});\
                    \n')
                else:
                    mock_file_h.write(f'DECLARE_FAKE_VOID_FUNC({function["function_name"]}, {", ".join(function["argument_types"])});\
                    \n')
            else:
                # DECLARE_FAKE_VALUE_FUNC(return_type, function_name, argument_types);
                # if function argument is void
                if function['argument_types'][0] == 'void':
                    mock_file_h.write(f'DECLARE_FAKE_VALUE_FUNC({function["return_type"]}, {function["function_name"]});\
                    \n')
                else:
                    mock_file_h.write(f'DECLARE_FAKE_VALUE_FUNC({function["return_type"]}, {function["function_name"]}, {", ".join(function["argument_types"])});\
                    \n')

        # write header to mock file .c
        mock_file_c.write(f'#include <{Path(file).stem}_mock.h>\n\n')

        # write mock function definitions to mock file .c
        for function in functions:
            # if function returns void
            if function['return_type'] == 'void':
                if function['argument_types'][0] == 'void':
                    # DEFINE_FAKE_VOID_FUNC(function_name)
                    mock_file_c.write(f'DEFINE_FAKE_VOID_FUNC({function["function_name"]});\
                    \n')
                else:
                    # DEFINE_FAKE_VOID_FUNC(function_name, argument_types)
                    mock_file_c.write(f'DEFINE_FAKE_VOID_FUNC({function["function_name"]}, {", ".join(function["argument_types"])});\
                    \n')

            else:                
                if function['argument_types'][0] == 'void':
                    mock_file_c.write(f'DEFINE_FAKE_VALUE_FUNC({function["return_type"]}, {function["function_name"]});\
                    \n')
                else:

                    # DEFINE_FAKE_VALUE_FUNC(return_type, function_name, argument_types);
                    mock_file_c.write(f'DEFINE_FAKE_VALUE_FUNC({function["return_type"]}, {function["function_name"]}, {", ".join(function["argument_types"])});\
                    \n')

        # close mock file .c and .h
        mock_file_c.close()
        mock_file_h.close()




if __name__ == "__main__":
    main()