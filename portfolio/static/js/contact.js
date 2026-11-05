const contactForm = document.getElementById("contactForm");

if (contactForm instanceof HTMLFormElement) {
    contactForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(contactForm);
        const name = String(formData.get("name") || "").trim();
        const email = String(formData.get("email") || "").trim();
        const subject = String(formData.get("subject") || "").trim();
        const message = String(formData.get("message") || "").trim();

        const body = [
            `Name: ${name}`,
            `Email: ${email}`,
            "",
            message,
        ].join("\n");
        const status = document.getElementById("contactFormStatus");
        if (status) {
            status.textContent = "Your email app will open with your message ready to send.";
        }

        window.location.href = `mailto:your-laurencemasika01@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });
}
