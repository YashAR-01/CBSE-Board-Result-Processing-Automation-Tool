import mysql.connector
import os
import csv

# ---------------- STEP 1: READ AND CLEAN RAW DATA ----------------
f = open("sample_result.txt", "r")
d = f.readlines()
f.close()

def notEmpty(x):
    return x.strip() != ""

d = list(filter(notEmpty, d))
l = []
inHeader = False
for i in range(len(d)):
    if not inHeader and d[i].startswith("----------------------"):
        inHeader = True
    if d[i-1].startswith("SCHOOL") and inHeader:
        inHeader = False
    if not inHeader:
        l.append(d[i])
d = l.copy()

if len(d) % 2 != 0:
    print("ERROR")

gp = [[d[i-1], d[i]] for i in range(1, len(d), 2)]

# Write cleaned data temporarily
f = open("out.txt", "w")
for i in d:
    f.write(i)
f.close()

# ---------------- STEP 2: LOAD SUBJECT CODES ----------------
f = open('list of codes.csv', 'r')
csv_obj = csv.reader(f)
codes = list(csv_obj)
f.close()

def assign_sub(code):
    for i in codes:
        if i[0] == code:
            return i[1]

# ---------------- STEP 3: FORMAT STUDENT DATA ----------------
f = open('out.txt', 'r')
data = f.readlines()
f.close()

new_data = []
for i in range(0, len(data), 2):
    details = data[i].split()
    name = ''
    c = 0
    for j in range(2, len(details)):
        if details[j-c].isalpha():
            if len(name) == 0:
                name += details[j-c]
            else:
                name += ' ' + details[j-c]
            details.pop(j-c)
            c += 1
        elif details[j].isdigit():
            break
    details.insert(2, name)
    marks = data[i+1].split()
    
    for k in range(0, len(marks), 2):
        x = details[3+k//2]
        x = assign_sub(x)
        sub_mark = {}
        sub_mark[x] = [int(marks[k]), marks[k+1]]
        details[3+k//2] = sub_mark
    new_data.append(details)

data = new_data

# Save structured data for debugging
with open("out.txt", "w") as f:
    f.writelines([(str(i) + "\n") for i in new_data])

# ---------------- STEP 4: MYSQL SETUP ----------------
conn = mysql.connector.connect(host="HOST", user="YOUR USERNAME", password="YOUR PASSWORD")
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS result_boards")
cursor.execute("CREATE DATABASE IF NOT EXISTS result_boards")
cursor.execute("USE result_boards")

# Create columns dynamically based on subjects
sub_ds_str = ""
with open("list of codes.csv") as sub:
    subs = sub.readlines()
    sub_l = []
    for i in subs:
        sub_l.append(i.split(",")[1].strip())
for i in sub_l:
    sub_ds_str += f',{i}_Marks int,{i}_Grade char(2)'

columns = f"""CREATE TABLE IF NOT EXISTS result(
    RollNo int PRIMARY KEY, 
    Gender CHAR(1), 
    name VARCHAR(100), 
    stream VARCHAR(50) 
    {sub_ds_str}, 
    BEST_4 FLOAT, 
    ALL_SUB FLOAT
);"""
cursor.execute(columns)
conn.commit()


# ---------------- STEP 5: HELPER FUNCTIONS ----------------
streams=[]

def get_stream(student):
    subjects = []
    for item in student[3:]:
        if type(item) is dict:
            subjects.append(list(item.keys())[0])
    science_subjects = ['Physics', 'Chemistry', 'Mathematics', 'Biology']
    commerce_subjects = ['Accountancy', 'Business_Studies', 'Economics', 'Mathematics']
    if 'Biology' in subjects:
        return "Med_Science"
    elif any([sub in subjects for sub in science_subjects]):
        return "Science"
    elif any([sub in subjects for sub in commerce_subjects]):
        return "Commerce"
    else:
        return "Arts"

def create_sql():
    """Insert or update student data into MySQL"""
    for student in new_data:
        roll_no, gender, name, stream = student[0], student[1], student[2], get_stream(student)
        l_marks = []
        # Check if roll_no exists
        cursor.execute("SELECT COUNT(*) FROM result WHERE RollNo = %s", (roll_no,))
        exists = cursor.fetchone()[0]
        if exists:
            resp = input(f"RollNo {roll_no} already exists. Update result? (y/n): ")
            if resp.lower() != 'y':
                print(f"Skipping RollNo {roll_no}")
                continue
            cursor.execute("UPDATE result SET Gender=%s, name=%s, stream=%s WHERE RollNo=%s",
                           (gender, name, stream, roll_no))
            conn.commit()
        else:
            cursor.execute('INSERT INTO result(RollNo,Gender,name,stream) VALUES (%s,%s,%s,%s)',
                           (roll_no, gender, name, stream))
            conn.commit()
        
        for sub in student[3::]:
            if str(type(sub)) == "<class 'dict'>":
                sub_str = str(list(sub.keys())[0])
                grade = sub_str + '_Grade'
                marks = sub_str + '_Marks'
                query = f"""INSERT INTO result (RollNo,{marks},{grade}) 
                            VALUES (%s,%s,%s) 
                            ON DUPLICATE KEY UPDATE {marks}=VALUES({marks}),{grade}=VALUES({grade})"""
                values = (roll_no, sub[sub_str][0], sub[sub_str][1])
                l_marks.append(int(sub[sub_str][0]))
                cursor.execute(query, values)
                conn.commit()
        l_marks.sort(reverse=True)
        best4 = int((sum(l_marks[:4:])/4)*100)
        all_sub = int((sum(l_marks)/len(l_marks))*100)
        query = 'UPDATE result set BEST_4=%s, ALL_SUB=%s WHERE RollNo=%s'
        values = (best4/100, all_sub/100, roll_no)
        cursor.execute(query, values)
        conn.commit()

def generate_streamwise_tables():
    global streams
    """Create separate tables for each stream"""
    cursor.execute("SELECT DISTINCT stream FROM result")
    streams = [i[0] for i in cursor.fetchall()]
    print(streams)
    for stream in streams:
        stream_name = stream
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {stream_name}_result 
                           AS SELECT * FROM result WHERE stream = '{stream_name}'""")
        conn.commit()

def qpi_calculator(table_name):
    query=f'SELECT SUM(ALL_SUB) FROM {table_name}'
    cursor.execute(query)
    total_marks=cursor.fetchall()[0][0]
    query=f'SELECT COUNT(ALL_SUB) FROM {table_name}'
    cursor.execute(query)
    total_max=cursor.fetchall()[0][0]
    return(total_marks/total_max)

# ---------------- STEP 6: CLEANED FUNCTIONS WITH MENU ----------------
def generate_csv(table_name, filename, sort_option):
    """Generate CSV for a given table sorted as per user choice"""
    if sort_option == 1:
        query = f"SELECT * FROM {table_name} ORDER BY BEST_4 DESC"
    elif sort_option == 2:
        query = f"SELECT * FROM {table_name} ORDER BY ALL_SUB DESC"
    else:
        query = f"SELECT * FROM {table_name} ORDER BY RollNo ASC"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    with open(filename, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # headers
        csv_writer.writerows(rows)
    
    print(f"\n✅ CSV generated: {filename}\n")

def table_refactor(table_name="result"):
    """Drop columns where all entries are NULL"""
    cursor.execute(f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'result_boards'
    """)
    columns = cursor.fetchall()
    
    for column in columns:
        col_name = column[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} IS NOT NULL")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {col_name}")
            conn.commit()
            #print(f"🗑 Dropped empty column: {col_name}")

def list_tables():
    """Fetch all result-related tables"""
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall() if t[0].endswith("_result") or t[0] == "result"]
    n=tables.index("result")
    tables[0],tables[n]=tables[n],tables[0]
    
    return tables

def menu():
    """Menu-driven interface for generating CSVs"""
    while True:
        print("\n📊 Available Functions:")
        tables = list_tables()
        print("0. Exit")
        print("1. QPI")
        for idx, table in enumerate(tables, 2):
            print(f"{idx}. {table}")
        
        
        try:
            choice = int(input("\nSelect a table: "))
        except ValueError:
            print("❌ Invalid input. Try again.")
            continue
        if choice == 0:
            print("👋 Exiting...")
            break

        elif choice==1:
            print('\nDISPLAYING QPI TABLE/STREAM WISE\n')
            for i in tables:
                value=qpi_calculator(i)
                if i=='result':
                    i='All Streamers'
                print(f' {i}:{value}')
                

        
        elif 2 <= choice <= len(tables)+3:
            table_name = tables[choice-2]
            print(f"\n✅ Selected Table: {table_name}")
            print("\n🔽 Sorting Options:")
            print("1. Sort by BEST_4")
            print("2. Sort by ALL_SUB")
            print("3. Sort by RollNo (default)")
            
            try:
                sort_choice = int(input("\nChoose sorting option: "))
            except ValueError:
                sort_choice = 3  # default
            
            if sort_choice not in [1, 2, 3]:
                sort_choice = 3
            
            # Clean table before export
            table_refactor(table_name)
            
            # Generate CSV
            filename = f"{table_name}.csv"
            generate_csv(table_name, filename, sort_choice)
        else:
            print("❌ Invalid option. Try again.")

# ---------------- STEP 7: RUN EVERYTHING ----------------
create_sql()
generate_streamwise_tables()

if __name__ == "__main__":
    menu()
