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

// ==========================================
// AES CRYPTOGRAPHY
// ==========================================

const aesKey = document.getElementById("aes-key");
const aesText = document.getElementById("aes-text");

const aesEncryptButton = document.getElementById("aes-encrypt");
const aesDecryptButton = document.getElementById("aes-decrypt");
const aesClearButton = document.getElementById("aes-clear");
const aesCopyButton = document.getElementById("aes-copy");

const aesResult = document.getElementById("aes-result");
const aesMessage = document.getElementById("aes-message");


async function performAES(operation) {

    const key = aesKey.value.trim();
    const text = aesText.value;

    aesMessage.textContent = "";
    aesMessage.className = "crypto-message";


    if (!key) {

        showAESMessage("Please enter an AES key.", "error");
        return;

    }


    if (![16, 24, 32].includes(key.length)) {

        showAESMessage(
            "AES key must be exactly 16, 24, or 32 characters.",
            "error"
        );

        return;

    }


    if (!text.trim()) {

        showAESMessage("Please enter some text.", "error");
        return;

    }


    try {

        const response = await fetch("/api/aes", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                operation: operation,
                key: key,
                text: text

            })

        });


        const data = await response.json();


        if (!data.success) {

            showAESMessage(data.error, "error");
            return;

        }


        aesResult.value = data.result;

        showAESMessage(
            operation === "encrypt"
                ? "Text encrypted successfully."
                : "Text decrypted successfully.",
            "success"
        );


    } catch (error) {

        showAESMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

        console.error(error);

    }

}


function showAESMessage(message, type) {

    aesMessage.textContent = message;

    aesMessage.classList.add(type);

}


aesEncryptButton.addEventListener("click", () => {

    performAES("encrypt");

});


aesDecryptButton.addEventListener("click", () => {

    performAES("decrypt");

});


aesClearButton.addEventListener("click", () => {

    aesKey.value = "";
    aesText.value = "";
    aesResult.value = "";

    aesMessage.textContent = "";
    aesMessage.className = "crypto-message";

});


aesCopyButton.addEventListener("click", async () => {

    if (!aesResult.value) {

        showAESMessage(
            "There is no result to copy.",
            "error"
        );

        return;

    }


    await navigator.clipboard.writeText(aesResult.value);

    showAESMessage(
        "Result copied to clipboard.",
        "success"
    );

});