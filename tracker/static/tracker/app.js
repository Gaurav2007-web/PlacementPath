document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput && !dateInput.value) {
        const today = new Date();
        const localDate = new Date(
            today.getTime() - today.getTimezoneOffset() * 60000
        ).toISOString().slice(0, 10);
        dateInput.value = localDate;
    }

    const links = document.querySelectorAll(".sidebar nav a");
    links.forEach(link => {
        link.addEventListener("click", () => {
            links.forEach(item => item.style.background = "");
            link.style.background = "#25304b";
        });
    });
});