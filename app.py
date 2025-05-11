import streamlit as st  # type: ignore
from fpdf import FPDF  # type: ignore
import tempfile
import os

# 🧱 Resume Class (OOP)
class Resume:
    def __init__(self, name, email, phone, summary, education, experience, skills):
        self.name = name
        self.email = email
        self.phone = phone
        self.summary = summary
        self.education = education
        self.experience = experience
        self.skills = skills.split(',') if skills else []

    def generate_pdf(self, image_file):
        pdf = FPDF()
        pdf.add_page()

        # 🖼️ Add Image (Top Center)
        if image_file:
            img_extension = os.path.splitext(image_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=img_extension) as tmp_img:
                tmp_img.write(image_file.read())
                tmp_img_path = tmp_img.name
            pdf.image(tmp_img_path, x=80, y=10, w=50)
            pdf.ln(55)
            os.remove(tmp_img_path)  # Clean up temporary file
        else:
            pdf.ln(20)

        # 📝 Add Name and Contact
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=self.name, ln=True, align='C')

        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Email: {self.email} | Phone: {self.phone}", ln=True, align='C')
        pdf.ln(10)

        # 📌 Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Professional Summary", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, self.summary)
        pdf.ln(5)

        # 🎓 Education
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Education", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, self.education)
        pdf.ln(5)

        # 💼 Experience
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Work Experience", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, self.experience)
        pdf.ln(5)

        # 🛠️ Skills
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Skills", ln=True)
        pdf.set_font("Arial", '', 12)
        for skill in self.skills:
            pdf.cell(0, 10, f"- {skill.strip()}", ln=True)

        return pdf.output(dest='S').encode('latin1')

# 🚀 Streamlit UI
def main():
    st.set_page_config(page_title="Stylish Resume Generator")
    st.title("📄 Stylish Resume Builder - Streamlit + OOP")

    image_file = st.file_uploader("Upload your profile image (PNG/JPG)", type=['png', 'jpg', 'jpeg'])

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    summary = st.text_area("Professional Summary")
    education = st.text_area("Education Background")
    experience = st.text_area("Work Experience")
    skills = st.text_area("Skills (comma separated, e.g., Python, HTML, CSS)")

    if st.button("Generate Resume"):
        if name and email and phone:
            resume = Resume(name, email, phone, summary, education, experience, skills)
            try:
                pdf_bytes = resume.generate_pdf(image_file)
                st.success("🎉 Resume generated successfully!")

                st.download_button(
                    label="📥 Download Resume PDF",
                    data=pdf_bytes,
                    file_name=f"{name.replace(' ', '_')}_resume.pdf",
                    mime='application/pdf'
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill in Name, Email, and Phone to continue.")

if __name__ == "__main__":
    main()
