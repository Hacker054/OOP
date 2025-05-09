from abc import ABC, abstractmethod
import os
import re
import sys

class Employee(ABC):
    """Lớp cơ sở Employee - lớp trừu tượng, không thể khởi tạo trực tiếp"""
    
    def __init__(self, employee_id, name, phone, email):
        if not is_valid_name(name):
            raise ValueError("Tên nhân viên không được để trống hoặc bắt đầu bằng số.")
        if not is_valid_phone(phone):
            raise ValueError("Số điện thoại không hợp lệ (chỉ chữ số, >=10 chữ số).")
            
        self.employee_id = employee_id
        self.name = name
        self.phone = phone
        self.email = email
    
    def display_info(self):
        """Hiển thị thông tin chung của nhân viên"""
        return f"ID: {self.employee_id}, Tên: {self.name}, SĐT: {self.phone}, Email: {self.email}"
    
    @abstractmethod
    def calculate_salary(self):
        """Phương thức trừu tượng, các lớp con phải triển khai"""
        pass
    
    @abstractmethod
    def to_txt_format(self):
        """Chuyển đối tượng thành chuỗi để lưu vào file text"""
        pass
    
    @classmethod
    @abstractmethod
    def from_txt_format(cls, txt_line):
        """Tạo đối tượng từ chuỗi text"""
        pass


class FullTimeEmployee(Employee):
    """Lớp nhân viên chính thức, kế thừa từ lớp Employee"""
    
    def __init__(self, employee_id, name, phone, email, base_salary, experience_years):
        super().__init__(employee_id, name, phone, email)
        
        if not isinstance(base_salary, (int, float)) or base_salary <= 0:
            raise ValueError("Lương cơ bản phải là số dương.")
        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Số năm kinh nghiệm phải là số nguyên không âm.")
            
        self.base_salary = base_salary
        self.experience_years = experience_years
    
    def calculate_salary(self):
        """Tính lương cho nhân viên chính thức dựa vào lương cơ bản và năm kinh nghiệm"""
        return self.base_salary * (1 + 0.1 * self.experience_years)
    
    def display_info(self):
        """Ghi đè phương thức display_info để hiển thị thêm thông tin"""
        basic_info = super().display_info()
        return f"{basic_info}, Lương cơ bản: {self.base_salary}, Năm kinh nghiệm: {self.experience_years}"
    
    def to_txt_format(self):
        """Chuyển đối tượng thành chuỗi để lưu vào file text"""
        return f"FullTime|{self.employee_id}|{self.name}|{self.phone}|{self.email}|{self.base_salary}|{self.experience_years}"
    
    @classmethod
    def from_txt_format(cls, txt_line):
        """Tạo đối tượng từ chuỗi text"""
        parts = txt_line.strip().split('|')
        if len(parts) < 7 or parts[0] != "FullTime":
            return None
        
        try:
            employee_id = parts[1]
            name = parts[2]
            phone = parts[3]
            email = parts[4]
            base_salary = float(parts[5])
            experience_years = int(parts[6])
            
            return cls(employee_id, name, phone, email, base_salary, experience_years)
        except (ValueError, IndexError):
            return None


class PartTimeEmployee(Employee):
    """Lớp nhân viên thời vụ, kế thừa từ lớp Employee"""
    
    def __init__(self, employee_id, name, phone, email, hourly_rate, working_hours):
        super().__init__(employee_id, name, phone, email)
        
        if not isinstance(hourly_rate, (int, float)) or hourly_rate <= 0:
            raise ValueError("Lương theo giờ phải là số dương.")
        if not isinstance(working_hours, (int, float)) or working_hours <= 0:
            raise ValueError("Số giờ làm việc phải là số dương.")
            
        self.hourly_rate = hourly_rate
        self.working_hours = working_hours
    
    def calculate_salary(self):
        """Tính lương cho nhân viên thời vụ dựa vào giờ làm và lương theo giờ"""
        return self.hourly_rate * self.working_hours
    
    def display_info(self):
        """Ghi đè phương thức display_info để hiển thị thêm thông tin"""
        basic_info = super().display_info()
        return f"{basic_info}, Lương theo giờ: {self.hourly_rate}, Số giờ làm việc: {self.working_hours}"
    
    def to_txt_format(self):
        """Chuyển đối tượng thành chuỗi để lưu vào file text"""
        return f"PartTime|{self.employee_id}|{self.name}|{self.phone}|{self.email}|{self.hourly_rate}|{self.working_hours}"
    
    @classmethod
    def from_txt_format(cls, txt_line):
        """Tạo đối tượng từ chuỗi text"""
        parts = txt_line.strip().split('|')
        if len(parts) < 7 or parts[0] != "PartTime":
            return None
        
        try:
            employee_id = parts[1]
            name = parts[2]
            phone = parts[3]
            email = parts[4]
            hourly_rate = float(parts[5])
            working_hours = float(parts[6])
            
            return cls(employee_id, name, phone, email, hourly_rate, working_hours)
        except (ValueError, IndexError):
            return None


class ManagerEmployee(FullTimeEmployee):
    """Lớp quản lý, kế thừa từ lớp FullTimeEmployee"""
    
    def __init__(self, employee_id, name, phone, email, base_salary, experience_years):
        super().__init__(employee_id, name, phone, email, base_salary, experience_years)
        self.team = []  # Danh sách nhân viên dưới quyền
    
    def add_employee(self, employee):
        """Thêm một nhân viên vào đội ngũ"""
        if employee.employee_id not in [e.employee_id for e in self.team]:
            self.team.append(employee)
            return True
        return False
    
    def remove_employee(self, employee_id):
        """Xóa nhân viên khỏi đội ngũ"""
        for i, employee in enumerate(self.team):
            if employee.employee_id == employee_id:
                self.team.pop(i)
                return True
        return False
    
    def display_team(self):
        """Hiển thị danh sách nhân viên trong đội"""
        result = f"Quản lý: {self.name} - Danh sách nhân viên ({len(self.team)}):\n"
        for employee in self.team:
            result += f"- {employee.display_info()}\n"
        return result
    
    def calculate_salary(self):
        """Tính lương cho quản lý (lương cơ bản + thưởng theo kinh nghiệm + thưởng quản lý)"""
        # Quản lý được thưởng thêm 20% lương cơ bản
        return super().calculate_salary() * 1.2
    
    def to_txt_format(self):
        """Chuyển đối tượng thành chuỗi để lưu vào file text"""
        # Base info
        result = f"Manager|{self.employee_id}|{self.name}|{self.phone}|{self.email}|{self.base_salary}|{self.experience_years}"
        
        # Add team members if any
        if self.team:
            team_ids = ';'.join([emp.employee_id for emp in self.team])
            result += f"|{team_ids}"
        
        return result
    
    @classmethod
    def from_txt_format(cls, txt_line):
        """Tạo đối tượng từ chuỗi text"""
        parts = txt_line.strip().split('|')
        if len(parts) < 7 or parts[0] != "Manager":
            return None
        
        try:
            employee_id = parts[1]
            name = parts[2]
            phone = parts[3]
            email = parts[4]
            base_salary = float(parts[5])
            experience_years = int(parts[6])
            
            manager = cls(employee_id, name, phone, email, base_salary, experience_years)
            
            # Add team member IDs if present
            if len(parts) > 7 and parts[7]:
                manager.team_ids = parts[7].split(';')
            else:
                manager.team_ids = []
            
            return manager
        except (ValueError, IndexError):
            return None


def is_valid_phone(phone):
    """
    Kiểm tra số điện thoại có hợp lệ hay không:
    - Chỉ chứa chữ số
    - Ít nhất 10 chữ số
    """
    return re.fullmatch(r'\d{10,}', phone) is not None


def is_valid_name(name):
    """
    Kiểm tra tên nhân viên:
    - Không được để trống
    - Không bắt đầu bằng số
    """
    return bool(name) and not name[0].isdigit()


class EmployeeManagementSystem:
    """Hệ thống quản lý nhân viên"""
    
    def __init__(self):
        self.employees = []
        self.data_file = "employees_data.txt"
        self.load_data()
    
    def add_employee(self, employee):
        """Thêm nhân viên mới vào hệ thống"""
        # Kiểm tra xem ID đã tồn tại chưa
        for emp in self.employees:
            if emp.employee_id == employee.employee_id:
                return False
        
        self.employees.append(employee)
        self.save_data()
        return True
    
    def update_employee(self, employee_id, updated_info):
        """Cập nhật thông tin nhân viên"""
        for i, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                # Cập nhật thông tin
                if hasattr(updated_info, 'name') and updated_info.name:
                    emp.name = updated_info.name
                if hasattr(updated_info, 'phone') and updated_info.phone:
                    emp.phone = updated_info.phone
                if hasattr(updated_info, 'email') and updated_info.email:
                    emp.email = updated_info.email
                
                # Cập nhật thông tin riêng cho từng loại nhân viên
                if isinstance(emp, FullTimeEmployee) and isinstance(updated_info, FullTimeEmployee):
                    if updated_info.base_salary > 0:
                        emp.base_salary = updated_info.base_salary
                    if updated_info.experience_years >= 0:
                        emp.experience_years = updated_info.experience_years
                
                elif isinstance(emp, PartTimeEmployee) and isinstance(updated_info, PartTimeEmployee):
                    if updated_info.hourly_rate > 0:
                        emp.hourly_rate = updated_info.hourly_rate
                    if updated_info.working_hours >= 0:
                        emp.working_hours = updated_info.working_hours
                
                self.save_data()
                return True
        return False
    
    def delete_employee(self, employee_id):
        """Xóa nhân viên khỏi hệ thống"""
        for i, emp in enumerate(self.employees):
            if emp.employee_id == employee_id:
                self.employees.pop(i)
                self.save_data()
                return True
        return False
    
    def find_employee_by_id(self, employee_id):
        """Tìm kiếm nhân viên theo ID"""
        for emp in self.employees:
            if emp.employee_id == employee_id:
                return emp
        return None
    
    def find_employee_by_name(self, name):
        """Tìm kiếm nhân viên theo tên"""
        result = []
        for emp in self.employees:
            if name.lower() in emp.name.lower():
                result.append(emp)
        return result
    
    def find_employee_by_phone(self, phone):
        """Tìm kiếm nhân viên theo số điện thoại"""
        for emp in self.employees:
            if phone in emp.phone:
                return emp
        return None
            
    def display_all_employees(self):
        """Hiển thị danh sách tất cả nhân viên"""
        if not self.employees:
            return "Không có nhân viên nào trong hệ thống."
        
        result = "DANH SÁCH NHÂN VIÊN:\n"
        for emp in self.employees:
            result += f"{emp.display_info()}\n"
        return result
    
    def display_employees_by_type(self, employee_type):
        """Hiển thị danh sách nhân viên theo loại"""
        result = []
        
        if employee_type == "FullTime":
            result = [emp for emp in self.employees if isinstance(emp, FullTimeEmployee) and not isinstance(emp, ManagerEmployee)]
        elif employee_type == "PartTime":
            result = [emp for emp in self.employees if isinstance(emp, PartTimeEmployee)]
        elif employee_type == "Manager":
            result = [emp for emp in self.employees if isinstance(emp, ManagerEmployee)]
        
        if not result:
            return f"Không có nhân viên {employee_type} nào trong hệ thống."
        
        output = f"DANH SÁCH NHÂN VIÊN {employee_type.upper()}:\n"
        for emp in result:
            output += f"{emp.display_info()}\n"
        return output
    
    def calculate_total_salary(self):
        """Tính tổng lương của tất cả nhân viên"""
        total_salary = 0
        for emp in self.employees:
            total_salary += emp.calculate_salary()
        return total_salary
    
    def calculate_total_salary_by_type(self, employee_type):
        """Tính tổng lương theo loại nhân viên"""
        total_salary = 0
        
        if employee_type == "FullTime":
            for emp in self.employees:
                if isinstance(emp, FullTimeEmployee) and not isinstance(emp, ManagerEmployee):
                    total_salary += emp.calculate_salary()
        elif employee_type == "PartTime":
            for emp in self.employees:
                if isinstance(emp, PartTimeEmployee):
                    total_salary += emp.calculate_salary()
        elif employee_type == "Manager":
            for emp in self.employees:
                if isinstance(emp, ManagerEmployee):
                    total_salary += emp.calculate_salary()
        
        return total_salary
    
    def get_top_salary_employees(self, n=3):
        """Lấy danh sách n nhân viên có lương cao nhất"""
        # Tạo list các tuple (employee, salary)
        emp_salary_list = [(emp, emp.calculate_salary()) for emp in self.employees]
        # Sắp xếp theo lương giảm dần
        emp_salary_list.sort(key=lambda x: x[1], reverse=True)
        # Trả về n nhân viên đầu tiên
        return emp_salary_list[:n]
    
    def save_data(self):
        """Lưu dữ liệu nhân viên vào file text"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # Đầu tiên lưu các nhân viên không phải quản lý
                for emp in self.employees:
                    if not isinstance(emp, ManagerEmployee):
                        f.write(emp.to_txt_format() + "\n")
                
                # Sau đó lưu các quản lý
                for emp in self.employees:
                    if isinstance(emp, ManagerEmployee):
                        f.write(emp.to_txt_format() + "\n")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi lưu file dữ liệu: {e}")
            return False
    
    def load_data(self):
        """Đọc dữ liệu nhân viên từ file text"""
        self.employees = []
        
        if not os.path.exists(self.data_file):
            print(f"File {self.data_file} không tồn tại. Tạo hệ thống mới.")
            return
        
        try:
            # Đọc tất cả các dòng từ file
            with open(self.data_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Đầu tiên, tạo tất cả các đối tượng nhân viên
            managers = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('|')
                if len(parts) < 2:
                    continue
                
                employee_type = parts[0]
                
                if employee_type == "FullTime":
                    emp = FullTimeEmployee.from_txt_format(line)
                    if emp:
                        self.employees.append(emp)
                
                elif employee_type == "PartTime":
                    emp = PartTimeEmployee.from_txt_format(line)
                    if emp:
                        self.employees.append(emp)
                
                elif employee_type == "Manager":
                    manager = ManagerEmployee.from_txt_format(line)
                    if manager:
                        self.employees.append(manager)
                        managers.append(manager)
            
            # Sau đó, thiết lập các đội nhóm cho quản lý
            for manager in managers:
                if hasattr(manager, 'team_ids') and manager.team_ids:
                    for emp_id in manager.team_ids:
                        emp = self.find_employee_by_id(emp_id)
                        if emp:
                            manager.add_employee(emp)
                    
                    # Xóa thuộc tính tạm thời
                    delattr(manager, 'team_ids')
            
            print(f"Đã đọc dữ liệu từ file {self.data_file} thành công.")
            return True
        
        except Exception as e:
            print(f"❌ Lỗi khi đọc file dữ liệu: {e}")
            return False


def input_fulltime():
    """
    Nhập thông tin cho nhân viên toàn thời gian.
    Mỗi field có vòng lặp riêng, chỉ re-prompt khi field đó sai.
    """
    try:
        emp_id = input("Nhập mã nhân viên: ").strip()
        
        # name
        while True:
            name = input("Nhập tên nhân viên: ").strip()
            if is_valid_name(name):
                break
            print("❌ Lỗi: Tên nhân viên không được để trống hoặc bắt đầu bằng số.")

        email = input("Nhập email: ").strip()

        # base_salary
        while True:
            s = input("Nhập lương cơ bản: ").strip()
            try:
                base_salary = float(s)
                if base_salary <= 0:
                    print("❌ Lỗi: Lương cơ bản phải là số dương.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Lương cơ bản phải là số.")

        # exp
        while True:
            s = input("Nhập số năm kinh nghiệm: ").strip()
            try:
                exp = int(s)
                if exp < 0:
                    print("❌ Lỗi: Số năm kinh nghiệm không được âm.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Số năm kinh nghiệm phải là số nguyên.")

        # phone và constructor
        while True:
            phone = input("Nhập số điện thoại: ").strip()
            if not is_valid_phone(phone):
                print("❌ Lỗi: Số điện thoại không hợp lệ (chỉ chữ số, >=10 chữ số).")
                continue
            try:
                emp = FullTimeEmployee(emp_id, name, phone, email, base_salary, exp)
                return emp
            except ValueError as e:
                print(f"❌ Lỗi: {e}")
                continue

    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ nhập liệu.")
        return None
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")
        return None


def input_parttime():
    """
    Nhập thông tin cho nhân viên bán thời gian.
    Mỗi field có vòng lặp riêng, chỉ re-prompt khi field đó sai.
    """
    try:
        emp_id = input("Nhập mã nhân viên: ").strip()
        
        # name
        while True:
            name = input("Nhập tên nhân viên: ").strip()
            if is_valid_name(name):
                break
            print("❌ Lỗi: Tên nhân viên không được để trống hoặc bắt đầu bằng số.")

        email = input("Nhập email: ").strip()

        # hours
        while True:
            s = input("Nhập số giờ làm việc: ").strip()
            try:
                hours = float(s)
                if hours <= 0:
                    print("❌ Lỗi: Số giờ làm việc phải là số dương.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Số giờ làm việc phải là số.")

        # wage
        while True:
            s = input("Nhập lương theo giờ: ").strip()
            try:
                wage = float(s)
                if wage <= 0:
                    print("❌ Lỗi: Lương theo giờ phải là số dương.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Lương theo giờ phải là số.")

        # phone và constructor
        while True:
            phone = input("Nhập số điện thoại: ").strip()
            if not is_valid_phone(phone):
                print("❌ Lỗi: Số điện thoại không hợp lệ (chỉ chữ số, >=10 chữ số).")
                continue
            try:
                emp = PartTimeEmployee(emp_id, name, phone, email, wage, hours)
                return emp
            except ValueError as e:
                print(f"❌ Lỗi: {e}")
                continue

    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ nhập liệu.")
        return None
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")
        return None


def input_manager():
    """
    Nhập thông tin cho nhân viên quản lý.
    Mỗi field có vòng lặp riêng, chỉ re-prompt khi field đó sai.
    """
    try:
        emp_id = input("Nhập mã nhân viên: ").strip()
        
        # name
        while True:
            name = input("Nhập tên nhân viên: ").strip()
            if is_valid_name(name):
                break
            print("❌ Lỗi: Tên nhân viên không được để trống hoặc bắt đầu bằng số.")

        email = input("Nhập email: ").strip()

        # base_salary
        while True:
            s = input("Nhập lương cơ bản: ").strip()
            try:
                base_salary = float(s)
                if base_salary <= 0:
                    print("❌ Lỗi: Lương cơ bản phải là số dương.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Lương cơ bản phải là số.")

        # exp
        while True:
            s = input("Nhập số năm kinh nghiệm: ").strip()
            try:
                exp = int(s)
                if exp < 0:
                    print("❌ Lỗi: Số năm kinh nghiệm không được âm.")
                    continue
                break
            except ValueError:
                print("❌ Lỗi: Số năm kinh nghiệm phải là số nguyên.")

        # phone và constructor
        while True:
            phone = input("Nhập số điện thoại: ").strip()
            if not is_valid_phone(phone):
                print("❌ Lỗi: Số điện thoại không hợp lệ (chỉ chữ số, >=10 chữ số).")
                continue
            try:
                emp = ManagerEmployee(emp_id, name, phone, email, base_salary, exp)
                return emp
            except ValueError as e:
                print(f"❌ Lỗi: {e}")
                continue

    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ nhập liệu.")
        return None
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")
        return None


def add_employee_menu(system):
    """Menu thêm nhân viên mới"""
    try:
        print("\n----- THÊM NHÂN VIÊN MỚI -----")
        print("1. Nhân viên chính thức")
        print("2. Nhân viên thời vụ")
        print("3. Nhân viên quản lý")
        print("0. Quay lại")
        
        choice = input("Chọn loại nhân viên: ").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            nv = input_fulltime()
            if nv:
                if system.add_employee(nv):
                    print("✅ Đã thêm nhân viên toàn thời gian thành công.")
                else:
                    print("❌ Lỗi: Mã nhân viên đã tồn tại.")
        elif choice == "2":
            nv = input_parttime()
            if nv:
                if system.add_employee(nv):
                    print("✅ Đã thêm nhân viên bán thời gian thành công.")
                else:
                    print("❌ Lỗi: Mã nhân viên đã tồn tại.")
        elif choice == "3":
            nv = input_manager()
            if nv:
                if system.add_employee(nv):
                    print("✅ Đã thêm nhân viên quản lý thành công.")
                else:
                    print("❌ Lỗi: Mã nhân viên đã tồn tại.")
        else:
            print("❌ Lỗi: Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, 3 hoặc 0.")
    
    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ thao tác thêm nhân viên.")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")


def update_employee_menu(system):
    """Menu cập nhật thông tin nhân viên"""
    try:
        print("\n----- CẬP NHẬT THÔNG TIN NHÂN VIÊN -----")
        
        while True:
            employee_id = input("Nhập mã nhân viên cần cập nhật (0 để quay lại): ").strip()
            
            if employee_id == "0":
                return
                
            employee = system.find_employee_by_id(employee_id)
            if not employee:
                print("❌ Không tìm thấy nhân viên với mã này.")
                continue
                
            print(f"Thông tin hiện tại: {employee.display_info()}")
            print("\nNhập thông tin mới (để trống nếu không thay đổi):")
            
            # Nhập các thông tin cơ bản
            name = input("Tên mới: ").strip()
            phone = input("Số điện thoại mới: ").strip()
            if phone and not is_valid_phone(phone):
                print("❌ Số điện thoại không hợp lệ. Bỏ qua cập nhật SĐT.")
                phone = ""
                
            email = input("Email mới: ").strip()
            
            # Tạo đối tượng cập nhật tương ứng với loại nhân viên
            if isinstance(employee, ManagerEmployee):
                base_salary_str = input("Lương cơ bản mới: ").strip()
                base_salary = float(base_salary_str) if base_salary_str else 0
                
                exp_str = input("Số năm kinh nghiệm mới: ").strip()
                exp = int(exp_str) if exp_str else 0
                
                updated_info = ManagerEmployee("temp", name or employee.name, 
                                              phone or employee.phone, 
                                              email or employee.email,
                                              base_salary, exp)
                
            elif isinstance(employee, FullTimeEmployee):
                base_salary_str = input("Lương cơ bản mới: ").strip()
                base_salary = float(base_salary_str) if base_salary_str else 0
                
                exp_str = input("Số năm kinh nghiệm mới: ").strip()
                exp = int(exp_str) if exp_str else 0
                
                updated_info = FullTimeEmployee("temp", name or employee.name, 
                                              phone or employee.phone, 
                                              email or employee.email,
                                              base_salary, exp)
                
            elif isinstance(employee, PartTimeEmployee):
                hourly_rate_str = input("Lương theo giờ mới: ").strip()
                hourly_rate = float(hourly_rate_str) if hourly_rate_str else 0
                
                hours_str = input("Số giờ làm việc mới: ").strip()
                hours = float(hours_str) if hours_str else 0
                
                updated_info = PartTimeEmployee("temp", name or employee.name, 
                                              phone or employee.phone, 
                                              email or employee.email,
                                              hourly_rate, hours)
            
            # Thực hiện cập nhật
            if system.update_employee(employee_id, updated_info):
                print("✅ Cập nhật thông tin nhân viên thành công!")
            else:
                print("❌ Cập nhật thông tin thất bại.")
            
            break
            
    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ thao tác cập nhật.")
    except ValueError as e:
        print(f"❌ Lỗi giá trị: {e}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")


def delete_employee_menu(system):
    """Menu xóa nhân viên"""
    try:
        print("\n----- XÓA NHÂN VIÊN -----")
        
        employee_id = input("Nhập mã nhân viên cần xóa (0 để quay lại): ").strip()
        
        if employee_id == "0":
            return
            
        employee = system.find_employee_by_id(employee_id)
        if not employee:
            print("❌ Không tìm thấy nhân viên với mã này.")
            return
            
        print(f"Thông tin nhân viên: {employee.display_info()}")
        confirm = input("Bạn có chắc chắn muốn xóa nhân viên này? (y/n): ").strip().lower()
        
        if confirm == 'y':
            if system.delete_employee(employee_id):
                print("✅ Đã xóa nhân viên thành công.")
            else:
                print("❌ Xóa nhân viên thất bại.")
        else:
            print("⚠️  Hủy bỏ thao tác xóa nhân viên.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ thao tác xóa nhân viên.")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")


def search_employee_menu(system):
    """Menu tìm kiếm nhân viên"""
    try:
        print("\n----- TÌM KIẾM NHÂN VIÊN -----")
        print("1. Tìm kiếm theo mã nhân viên")
        print("2. Tìm kiếm theo tên")
        print("3. Tìm kiếm theo số điện thoại")
        print("0. Quay lại")
        
        choice = input("Chọn cách tìm kiếm: ").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            employee_id = input("Nhập mã nhân viên cần tìm: ").strip()
            employee = system.find_employee_by_id(employee_id)
            
            if employee:
                print("\nKẾT QUẢ TÌM KIẾM:")
                print(employee.display_info())
            else:
                print("❌ Không tìm thấy nhân viên với mã này.")
                
        elif choice == "2":
            name = input("Nhập tên nhân viên cần tìm: ").strip()
            employees = system.find_employee_by_name(name)
            
            if employees:
                print("\nKẾT QUẢ TÌM KIẾM:")
                for emp in employees:
                    print(emp.display_info())
            else:
                print("❌ Không tìm thấy nhân viên nào có tên này.")
                
        elif choice == "3":
            phone = input("Nhập số điện thoại cần tìm: ").strip()
            employee = system.find_employee_by_phone(phone)
            
            if employee:
                print("\nKẾT QUẢ TÌM KIẾM:")
                print(employee.display_info())
            else:
                print("❌ Không tìm thấy nhân viên với số điện thoại này.")
                
        else:
            print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, 3 hoặc 0.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ thao tác tìm kiếm.")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")


def manage_team_menu(system):
    """Menu quản lý đội nhóm cho quản lý"""
    try:
        print("\n----- QUẢN LÝ ĐỘI NHÓM -----")
        
        # Tìm quản lý
        manager_id = input("Nhập mã nhân viên quản lý (0 để quay lại): ").strip()
        
        if manager_id == "0":
            return
            
        manager = system.find_employee_by_id(manager_id)
        if not manager:
            print("❌ Không tìm thấy nhân viên với mã này.")
            return
            
        if not isinstance(manager, ManagerEmployee):
            print("❌ Nhân viên này không phải là quản lý.")
            return
            
        while True:
            print(f"\nQuản lý: {manager.name}")
            print("1. Xem danh sách nhân viên trong đội")
            print("2. Thêm nhân viên vào đội")
            print("3. Xóa nhân viên khỏi đội")
            print("0. Quay lại")
            
            choice = input("Chọn thao tác: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                print(manager.display_team())
            elif choice == "2":
                employee_id = input("Nhập mã nhân viên cần thêm vào đội: ").strip()
                employee = system.find_employee_by_id(employee_id)
                
                if not employee:
                    print("❌ Không tìm thấy nhân viên với mã này.")
                    continue
                    
                if isinstance(employee, ManagerEmployee):
                    print("❌ Không thể thêm quản lý vào đội.")
                    continue
                    
                if manager.add_employee(employee):
                    system.save_data()  # Lưu thay đổi
                    print(f"✅ Đã thêm nhân viên {employee.name} vào đội của {manager.name}.")
                else:
                    print("❌ Nhân viên đã trong đội hoặc có lỗi xảy ra.")
                    
            elif choice == "3":
                employee_id = input("Nhập mã nhân viên cần xóa khỏi đội: ").strip()
                
                if manager.remove_employee(employee_id):
                    system.save_data()  # Lưu thay đổi
                    print("✅ Đã xóa nhân viên khỏi đội.")
                else:
                    print("❌ Không tìm thấy nhân viên trong đội.")
            else:
                print("❌ Lựa chọn không hợp lệ.")
    
    except KeyboardInterrupt:
        print("\n⚠️  Hủy bỏ thao tác quản lý đội nhóm.")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")


def salary_statistics_menu(system):
    """Menu thống kê lương"""
    try:
        print("\n----- THỐNG KÊ LƯƠNG -----")
        print(f"Tổng quỹ lương: {system.calculate_total_salary():,.2f}")
        print(f"Tổng lương nhân viên chính thức: {system.calculate_total_salary_by_type('FullTime'):,.2f}")
        print(f"Tổng lương nhân viên thời vụ: {system.calculate_total_salary_by_type('PartTime'):,.2f}")
        print(f"Tổng lương quản lý: {system.calculate_total_salary_by_type('Manager'):,.2f}")
        
        print("\nTop 3 nhân viên lương cao nhất:")
        top_employees = system.get_top_salary_employees(3)
        for i, (emp, salary) in enumerate(top_employees, 1):
            print(f"{i}. {emp.name} - {salary:,.2f}")
            
    except Exception as e:
        print(f"❌ Lỗi khi thống kê lương: {e}")


def init_sample_data(system):
    """Khởi tạo dữ liệu mẫu cho hệ thống"""
    try:
        # Tạo nhân viên chính thức
        ft1 = FullTimeEmployee("FT001", "Nguyễn Văn An", "0912345678", "an@example.com", 10000000, 3)
        ft2 = FullTimeEmployee("FT002", "Trần Thị Bình", "0923456789", "binh@example.com", 12000000, 5)
        
        # Tạo nhân viên thời vụ
        pt1 = PartTimeEmployee("PT001", "Lê Văn Cường", "0934567890", "cuong@example.com", 100000, 80)
        pt2 = PartTimeEmployee("PT002", "Phạm Thị Dung", "0945678901", "dung@example.com", 120000, 60)
        
        # Tạo quản lý
        m1 = ManagerEmployee("M001", "Hoàng Văn Em", "0956789012", "em@example.com", 20000000, 7)
        m2 = ManagerEmployee("M002", "Trương Thị Phương", "0967890123", "phuong@example.com", 22000000, 8)
        
        # Thêm vào hệ thống
        system.add_employee(ft1)
        system.add_employee(ft2)
        system.add_employee(pt1)
        system.add_employee(pt2)
        system.add_employee(m1)
        system.add_employee(m2)
        
        # Thêm nhân viên vào đội
        m1.add_employee(ft1)
        m1.add_employee(pt1)
        m2.add_employee(ft2)
        m2.add_employee(pt2)
        
        # Lưu dữ liệu
        system.save_data()
        print("✅ Đã khởi tạo dữ liệu mẫu thành công.")
        
    except Exception as e:
        print(f"❌ Lỗi khi khởi tạo dữ liệu mẫu: {e}")


def main_menu():
    """Menu chính của chương trình"""
    system = EmployeeManagementSystem()
    
    while True:
        try:
            print("\n===== HỆ THỐNG QUẢN LÝ NHÂN VIÊN =====")
            print("1. Xem danh sách nhân viên")
            print("2. Thêm nhân viên mới")
            print("3. Cập nhật thông tin nhân viên")
            print("4. Xóa nhân viên")
            print("5. Tìm kiếm nhân viên")
            print("6. Quản lý đội nhóm")
            print("7. Thống kê lương")
            print("8. Khởi tạo dữ liệu mẫu")
            print("0. Thoát chương trình")
            
            choice = input("\nChọn chức năng: ").strip()
            
            if choice == "0":
                print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
                break
            elif choice == "1":
                print("\n----- DANH SÁCH NHÂN VIÊN -----")
                print("1. Tất cả nhân viên")
                print("2. Nhân viên chính thức")
                print("3. Nhân viên thời vụ")
                print("4. Quản lý")
                print("0. Quay lại")
                
                sub_choice = input("Chọn loại nhân viên: ").strip()
                
                if sub_choice == "0":
                    continue
                elif sub_choice == "1":
                    print(system.display_all_employees())
                elif sub_choice == "2":
                    print(system.display_employees_by_type("FullTime"))
                elif sub_choice == "3":
                    print(system.display_employees_by_type("PartTime"))
                elif sub_choice == "4":
                    print(system.display_employees_by_type("Manager"))
                else:
                    print("❌ Lựa chọn không hợp lệ.")
                    
            elif choice == "2":
                add_employee_menu(system)
            elif choice == "3":
                update_employee_menu(system)
            elif choice == "4":
                delete_employee_menu(system)
            elif choice == "5":
                search_employee_menu(system)
            elif choice == "6":
                manage_team_menu(system)
            elif choice == "7":
                salary_statistics_menu(system)
            elif choice == "8":
                init_sample_data(system)
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn lại.")
                
        except KeyboardInterrupt:
            print("\n⚠️  Thoát chương trình...")
            break
        except Exception as e:
            print(f"❌ Lỗi không mong muốn: {e}")


if __name__ == "__main__":
    # Chạy chương trình
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n⚠️  Chương trình đã bị dừng bởi người dùng.")
    except Exception as e:
        print(f"❌ Lỗi nghiêm trọng: {e}")
        sys.exit(1)