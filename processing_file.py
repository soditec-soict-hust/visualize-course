import pandas as pd

# columns = ['Timestamp', 'Email address', 'Họ và tên',
#        'Bạn có phải là sinh viên Đại học Bách khoa Hà Nội không',
#        'Tên trường bạn đang học\nVD: Đại học Bách Khoa Hà Nội', 'Giới tính',
#        'Link Facebook', 'Email dùng đăng nhập https://hocbk.daotao.ai',
#        'Mã số sinh viên\nStudent ID', 'Lớp\nClass\nVD: IT1-05-K68',
#        'Kiểm tra share', 'Kiểm tra add', 'Đã gửi Email nhắc share',
#        'Gửi link nhóm hỗ trợ', 'check share tạm thời']

def processing_file(file, file_type):

    if file_type == 'text/csv':
        df = pd.read_csv(file)
    elif file_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        df = pd.read_excel(file)
    df['Lớp\nClass\nVD: IT1-05-K68'] = df['Lớp\nClass\nVD: IT1-05-K68'].apply(lambda x: str(x).upper())
    data = pd.DataFrame(columns=["Time", "Day", "IsHust", "MSSV", "Class", "Grade", "Sex"])
    data["Time"] = pd.to_datetime(df['Timestamp']).dt.hour
    data["Day"] = pd.to_datetime(df['Timestamp']).dt.date
    data["IsHust"] = df['Bạn có phải là sinh viên Đại học Bách khoa Hà Nội không'].apply(lambda x: "Yes" if x == "Có" else "No")
    data["MSSV"] = df['Mã số sinh viên\nStudent ID']
    data['Sex'] = df['Giới tính']
    data[['Class', 'Grade']] = df['Lớp\nClass\nVD: IT1-05-K68'].str.extract(r'([A-Z0-9]+)-\d+-([A-Z0-9]+)')
    data["Class"] = data["Class"].apply(lambda x: x if len(str(x)) > 1 else None)
    return data # columns
