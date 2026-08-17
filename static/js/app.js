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
            rsaWorkspace.style.display = "none";

        } else if (tab.id === "rsa-tab") {

            aesWorkspace.style.display = "none";
            desWorkspace.style.display = "none";
            rsaWorkspace.style.display = "block";

        } else {

            aesWorkspace.style.display = "block";
            desWorkspace.style.display = "none";
            rsaWorkspace.style.display = "none";

        }

    });

});

// ==========================================
// RSA CRYPTOGRAPHY
// ==========================================

const rsaTab = document.getElementById("rsa-tab");
const rsaWorkspace = document.getElementById("rsa-workspace");

const rsaGenerateButton = document.getElementById("rsa-generate");

const rsaPublicKey = document.getElementById("rsa-public-key");
const rsaPrivateKey = document.getElementById("rsa-private-key");

const rsaCopyPublic = document.getElementById("rsa-copy-public");
const rsaCopyPrivate = document.getElementById("rsa-copy-private");

const rsaText = document.getElementById("rsa-text");

const rsaEncryptButton = document.getElementById("rsa-encrypt");
const rsaDecryptButton = document.getElementById("rsa-decrypt");
const rsaClearButton = document.getElementById("rsa-clear");

const rsaMessage = document.getElementById("rsa-message");
const rsaResult = document.getElementById("rsa-result");
const rsaCopyResult = document.getElementById("rsa-copy-result");


function showRSAMessage(message, type) {

    rsaMessage.textContent = message;

    rsaMessage.className = "crypto-message";

    rsaMessage.classList.add(type);
}


// ==========================================
// GENERATE RSA KEYS
// ==========================================

rsaGenerateButton.addEventListener("click", async () => {

    showRSAMessage("Generating 2048-bit RSA keys...", "success");

    rsaGenerateButton.disabled = true;

    try {

        const response = await fetch(
            "/api/rsa/generate",
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!data.success) {

            showRSAMessage(
                data.error,
                "error"
            );

            return;
        }

        rsaPublicKey.value = data.public_key;
        rsaPrivateKey.value = data.private_key;

        rsaResult.value = "";

        showRSAMessage(
            "RSA key pair generated successfully.",
            "success"
        );

    } catch (error) {

        console.error(error);

        showRSAMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    } finally {

        rsaGenerateButton.disabled = false;

    }

});


// ==========================================
// RSA ENCRYPT / DECRYPT
// ==========================================

async function performRSA(operation) {

    const text = rsaText.value.trim();

    let key;


    if (operation === "encrypt") {

        key = rsaPublicKey.value.trim();

    } else {

        key = rsaPrivateKey.value.trim();

    }


    if (!key) {

        showRSAMessage(
            operation === "encrypt"
                ? "Generate or enter a public key first."
                : "Generate or enter a private key first.",
            "error"
        );

        return;
    }


    if (!text) {

        showRSAMessage(
            "Please enter some text.",
            "error"
        );

        return;
    }


    try {

        const response = await fetch(
            "/api/rsa",
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

            showRSAMessage(
                data.error,
                "error"
            );

            return;

        }


        rsaResult.value = data.result;


        showRSAMessage(

            operation === "encrypt"
                ? "Text encrypted successfully."
                : "Text decrypted successfully.",

            "success"

        );


    } catch (error) {

        console.error(error);

        showRSAMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    }

}


// Encrypt

rsaEncryptButton.addEventListener(
    "click",
    () => {

        performRSA("encrypt");

    }
);


// Decrypt

rsaDecryptButton.addEventListener(
    "click",
    () => {

        performRSA("decrypt");

    }
);


// ==========================================
// COPY BUTTONS
// ==========================================

rsaCopyPublic.addEventListener(
    "click",
    async () => {

        if (!rsaPublicKey.value) {

            showRSAMessage(
                "No public key available.",
                "error"
            );

            return;
        }

        await navigator.clipboard.writeText(
            rsaPublicKey.value
        );

        showRSAMessage(
            "Public key copied to clipboard.",
            "success"
        );

    }
);


rsaCopyPrivate.addEventListener(
    "click",
    async () => {

        if (!rsaPrivateKey.value) {

            showRSAMessage(
                "No private key available.",
                "error"
            );

            return;
        }

        await navigator.clipboard.writeText(
            rsaPrivateKey.value
        );

        showRSAMessage(
            "Private key copied to clipboard.",
            "success"
        );

    }
);


rsaCopyResult.addEventListener(
    "click",
    async () => {

        if (!rsaResult.value) {

            showRSAMessage(
                "There is no result to copy.",
                "error"
            );

            return;
        }

        await navigator.clipboard.writeText(
            rsaResult.value
        );

        showRSAMessage(
            "Result copied to clipboard.",
            "success"
        );

    }
);


// ==========================================
// CLEAR RSA
// ==========================================

rsaClearButton.addEventListener(
    "click",
    () => {

        rsaText.value = "";

        rsaResult.value = "";

        rsaMessage.textContent = "";

        rsaMessage.className = "crypto-message";

    }
);

// ==========================================
// SHA-256 HASHING
// ==========================================

const hashText = document.getElementById("hash-text");
const hashGenerateButton = document.getElementById("hash-generate");
const hashClearButton = document.getElementById("hash-clear");
const hashCopyButton = document.getElementById("hash-copy");

const hashResult = document.getElementById("hash-result");
const hashMessage = document.getElementById("hash-message");


function showHashMessage(message, type) {

    hashMessage.textContent = message;

    hashMessage.className = "crypto-message";

    hashMessage.classList.add(type);

}


async function generateSHA256() {

    const text = hashText.value;

    hashMessage.textContent = "";
    hashMessage.className = "crypto-message";


    if (!text.trim()) {

        showHashMessage(
            "Please enter some text.",
            "error"
        );

        return;
    }


    try {

        const response = await fetch(
            "/api/hash",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            showHashMessage(
                data.error,
                "error"
            );

            return;
        }


        hashResult.value = data.result;


        showHashMessage(
            "SHA-256 hash generated successfully.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showHashMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    }

}


// Generate hash

hashGenerateButton.addEventListener(
    "click",
    () => {

        generateSHA256();

    }
);


// Clear

hashClearButton.addEventListener(
    "click",
    () => {

        hashText.value = "";

        hashResult.value = "";

        hashMessage.textContent = "";

        hashMessage.className = "crypto-message";

    }
);


// Copy hash

hashCopyButton.addEventListener(
    "click",
    async () => {

        if (!hashResult.value) {

            showHashMessage(
                "There is no hash to copy.",
                "error"
            );

            return;
        }


        await navigator.clipboard.writeText(
            hashResult.value
        );


        showHashMessage(
            "SHA-256 hash copied to clipboard.",
            "success"
        );

    }
);