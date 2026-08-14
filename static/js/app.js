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

// ==========================================
// DES CRYPTOGRAPHY
// ==========================================

const desTab = document.getElementById("des-tab");

const desWorkspace = document.getElementById("des-workspace");

const aesWorkspace = document.querySelector(
    ".crypto-workspace:not(#des-workspace)"
);


const desKey = document.getElementById("des-key");
const desText = document.getElementById("des-text");

const desEncryptButton =
    document.getElementById("des-encrypt");

const desDecryptButton =
    document.getElementById("des-decrypt");

const desClearButton =
    document.getElementById("des-clear");

const desCopyButton =
    document.getElementById("des-copy");

const desResult =
    document.getElementById("des-result");

const desMessage =
    document.getElementById("des-message");


function showDESMessage(message, type) {

    desMessage.textContent = message;

    desMessage.className = "crypto-message";

    desMessage.classList.add(type);

}


async function performDES(operation) {

    const key = desKey.value.trim();

    const text = desText.value;


    desMessage.textContent = "";

    desMessage.className = "crypto-message";


    if (!key) {

        showDESMessage(
            "Please enter a DES key.",
            "error"
        );

        return;

    }


    if (key.length !== 8) {

        showDESMessage(
            "DES key must be exactly 8 characters.",
            "error"
        );

        return;

    }


    if (!text.trim()) {

        showDESMessage(
            "Please enter some text.",
            "error"
        );

        return;

    }


    try {

        const response = await fetch(
            "/api/des",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    operation: operation,

                    key: key,

                    text: text

                })

            }
        );


        const data = await response.json();


        if (!data.success) {

            showDESMessage(
                data.error,
                "error"
            );

            return;

        }


        desResult.value = data.result;


        showDESMessage(

            operation === "encrypt"

                ? "Text encrypted successfully."

                : "Text decrypted successfully.",

            "success"

        );


    } catch (error) {

        showDESMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

        console.error(error);

    }

}


desEncryptButton.addEventListener(
    "click",
    () => {

        performDES("encrypt");

    }
);


desDecryptButton.addEventListener(
    "click",
    () => {

        performDES("decrypt");

    }
);


desClearButton.addEventListener(
    "click",
    () => {

        desKey.value = "";

        desText.value = "";

        desResult.value = "";

        desMessage.textContent = "";

        desMessage.className =
            "crypto-message";

    }
);


desCopyButton.addEventListener(
    "click",
    async () => {

        if (!desResult.value) {

            showDESMessage(
                "There is no result to copy.",
                "error"
            );

            return;

        }


        await navigator.clipboard.writeText(
            desResult.value
        );


        showDESMessage(
            "Result copied to clipboard.",
            "success"
        );

    }
);

// ==========================================
// CRYPTOGRAPHY TAB SWITCHING
// ==========================================

const cryptoTabs =
    document.querySelectorAll(".crypto-tab");


cryptoTabs.forEach((tab) => {

    tab.addEventListener("click", () => {

        cryptoTabs.forEach((item) => {

            item.classList.remove("active");

        });


        tab.classList.add("active");


        if (tab.id === "des-tab") {

            aesWorkspace.style.display = "none";

            desWorkspace.style.display = "block";

        } else {

            aesWorkspace.style.display = "block";

            desWorkspace.style.display = "none";

        }

    });

});