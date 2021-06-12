# Classroom-Manager
A django project which helps teachers to send notes to students in her class  

---

### Functionalities
- Accepts 3 different types of users : Student, Teacher and Officials
- Only officials can add another official
- Only officials can create a code for adding teacher
- Teachers have to use the code sent by the official to sign up as teacher
- Only teachers can add new class
- Every class has a code and teacher can sent that code to students and students can join class using that code
- Its basically like my own version of Google Classroom :sweat_smile:

---

### How to Run
- create a virtual environment and activate it
- clone my project using `git clone https://github.com/NijoNinan/Classroom-Manager.git`
- run `pip install -r requirements.txt`
- run `cd MySchool`
- run `python manage.py runserver`
- open `http://127.0.0.1:8000/` on your favourite browser

---

### Note
The navbar is not ideal  
I have just added all my links in navbar for ease in access

---

### Pending Work
- Use Jquery to toggle display in `accounts/register.html`
- Apply on hover shadow to `class/templates` where `card` is used