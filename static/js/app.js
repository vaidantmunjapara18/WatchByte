const navItems = document.querySelectorAll(".nav-item");
const quickButtons = document.querySelectorAll(".quick-button");
const sections = document.querySelectorAll(".content-section");

const currentSection = document.getElementById("current-section");


function showSection(sectionId) {

    sections.forEach(section => {

        section.classList.remove("active-section");

    });


    const selectedSection = document.getElementById(sectionId);

    if (selectedSection) {

        selectedSection.classList.add("active-section");

    }


    navItems.forEach(item => {

        item.classList.remove("active");

        if (item.dataset.section === sectionId) {

            item.classList.add("active");

        }

    });


    currentSection.textContent = sectionId.toUpperCase();
}


/* Sidebar navigation */

navItems.forEach(item => {

    item.addEventListener("click", () => {

        showSection(item.dataset.section);

    });

});


/* Dashboard quick buttons */

quickButtons.forEach(button => {

    button.addEventListener("click", () => {

        showSection(button.dataset.section);

    });

});