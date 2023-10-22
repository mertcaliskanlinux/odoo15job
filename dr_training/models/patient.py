from odoo import models, fields, api  # Odoo's models, fields and API library. // Odoo'nun modül, alan ve API kütüphanesini içe aktar.
from odoo.exceptions import ValidationError  # Import ValidationError class from Odoo. // Odoo'dan hata doğrulama sınıfını içe aktar.

# a model for Patient. // Hasta için bir model.
class Patient(models.Model):
    _name = "dr_patients.patient"  # Name of the model. // Modelin adı.
    _description = "Patient"  # Description of the model. // Modelin açıklaması.
    _rec_name = "full_name"  # Name of the field representing model records. // Model kayıtlarını temsil eden alanın adı.

    # Create a unique ID for the patient. // Hasta için benzersiz bir kimlik oluştur.
    patient_id = fields.Char(
        string="Patient ID",  # Name displayed externally for this field. // Bu alan için dışarıda görünen adı.
        copy=False,  # Do not allow this field to be copied. // Bu alanın kopyalanmasına izin verme.
        readonly=True,  # This field is read-only. // Bu alan salt okunurdur.
        index=True,  # Index this field for faster searches. // Daha hızlı aramalar için bu alanı indeksle.
        default=lambda self: self.env['ir.sequence'].next_by_code('dr_patients.patient')  # Default method to generate unique IDs. // Benzersiz kimlikleri üretmek için varsayılan yöntem.
    )
    first_name = fields.Char(string="First Name", required=True)  # Field for the first name. // İsim için alan.
    last_name = fields.Char(string="Last Name", required=True)  # Field for the last name. // Soyisim için alan.
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)  # Field for the full name, computed from first and last name. // Tam ad için alan, ilk ad ve soyadından hesaplanır.
    date_of_birth = fields.Date(string="Date of Birth", required=True)  # Field for the date of birth. // Doğum tarihi için alan.
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")  # Field for age, computed from date of birth. // Yaş için alan, doğum tarihinden hesaplanır.
    address = fields.Text(string="Address", required=True)  # Field for the address. // Adres için alan.
    phone = fields.Char(string="Phone", required=True)  # Field for the phone number. // Telefon numarası için alan.
    email = fields.Char(string="Email", required=True)  # Field for the email address. // E-posta adresi için alan.
    national_id_no = fields.Char(string="National ID No.", required=True, unique=True)  # Field for the national ID number. // Ulusal kimlik numarası için alan.

    # Constrain to ensure national ID is unique. // Ulusal kimlik numarasının benzersiz olduğunu sağlamak için kısıtlama.
    @api.constrains('national_id_no')
    def _check_unique_national_id_no(self):
        for record in self:
            if record.national_id_no:
                existing_patient = self.env['dr_patients.patient'].search([
                    ('national_id_no', '=', record.national_id_no),
                    ('id', '!=', record.id),
                ])
                if existing_patient:
                    raise ValidationError("National ID No. must be unique.")  # Raise an error if a duplicate is found. // Bir çift bulunursa bir hata oluştur.

    # Compute age based on date of birth. // Doğum tarihine dayanarak yaş hesapla.
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.date_of_birth)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0

    # Compute full name from first and last name. // İlk ad ve soyadından tam adı hesapla.
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            if record.first_name and record.last_name:
                record.full_name = record.first_name + " " + record.last_name
            else:
                record.full_name = False
