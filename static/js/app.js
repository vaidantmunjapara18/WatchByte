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

// ==========================================
// HMAC-SHA256
// ==========================================

const hmacKey = document.getElementById("hmac-key");
const hmacText = document.getElementById("hmac-text");

const hmacGenerateButton =
    document.getElementById("hmac-generate");

const hmacClearButton =
    document.getElementById("hmac-clear");

const hmacCopyButton =
    document.getElementById("hmac-copy");

const hmacResult =
    document.getElementById("hmac-result");

const hmacMessage =
    document.getElementById("hmac-message");


function showHmacMessage(message, type) {

    hmacMessage.textContent = message;

    hmacMessage.className = "crypto-message";

    hmacMessage.classList.add(type);
}


async function generateHMAC() {

    const text = hmacText.value;
    const key = hmacKey.value;


    hmacMessage.textContent = "";
    hmacMessage.className = "crypto-message";


    if (!text.trim()) {

        showHmacMessage(
            "Please enter some text.",
            "error"
        );

        return;
    }


    if (!key.trim()) {

        showHmacMessage(
            "Please enter a secret key.",
            "error"
        );

        return;
    }


    try {

        const response = await fetch(
            "/api/hmac",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text,
                    key: key
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            showHmacMessage(
                data.error,
                "error"
            );

            return;
        }


        hmacResult.value = data.result;


        showHmacMessage(
            "HMAC generated successfully.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showHmacMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );
    }
}


// Generate HMAC

hmacGenerateButton.addEventListener(
    "click",
    () => {

        generateHMAC();

    }
);


// Clear HMAC

hmacClearButton.addEventListener(
    "click",
    () => {

        hmacKey.value = "";
        hmacText.value = "";
        hmacResult.value = "";

        hmacMessage.textContent = "";
        hmacMessage.className = "crypto-message";

    }
);


// Copy HMAC

hmacCopyButton.addEventListener(
    "click",
    async () => {

        if (!hmacResult.value) {

            showHmacMessage(
                "There is no HMAC to copy.",
                "error"
            );

            return;
        }


        await navigator.clipboard.writeText(
            hmacResult.value
        );


        showHmacMessage(
            "HMAC copied to clipboard.",
            "success"
        );

    }
);

// ==========================================
// FILE INTEGRITY - SHA-256
// ==========================================

const fileInput = document.getElementById("file-input");
const fileNameDisplay =
    document.getElementById("file-name-display");
const fileHashGenerateButton =
    document.getElementById("file-hash-generate");

const fileHashClearButton =
    document.getElementById("file-hash-clear");

const fileHashCopyButton =
    document.getElementById("file-hash-copy");

const fileHashResult =
    document.getElementById("file-hash-result");

const fileHashMessage =
    document.getElementById("file-hash-message");

const selectedFileName =
    document.getElementById("selected-file-name");


// Show selected filename

fileInput.addEventListener("change", function () {

    if (fileInput.files.length === 0) {

        fileNameDisplay.textContent =
            "📁 No file selected";

        selectedFileName.textContent =
            "No file selected";

        return;
    }

    const file = fileInput.files[0];

    fileNameDisplay.textContent =
        "📄 " + file.name;

    selectedFileName.textContent =
        file.name;

});


// Show file message

function showFileHashMessage(message, type) {

    fileHashMessage.textContent = message;

    fileHashMessage.className =
        "crypto-message";

    fileHashMessage.classList.add(type);
}


// Calculate file hash

async function calculateFileHash() {

    if (fileInput.files.length === 0) {

        showFileHashMessage(
            "Please select a file.",
            "error"
        );

        return;
    }


    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);


    try {

        const response = await fetch(
            "/api/file-hash",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!data.success) {

            showFileHashMessage(
                data.error,
                "error"
            );

            return;
        }


        fileHashResult.value = data.hash;


        showFileHashMessage(
            "File SHA-256 hash calculated successfully.",
            "success"
        );


    } catch (error) {

        console.error(error);

        showFileHashMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    }

}


// Calculate button

fileHashGenerateButton.addEventListener(
    "click",
    function () {

        calculateFileHash();

    }
);


// Clear

fileHashClearButton.addEventListener(
    "click",
    function () {

        fileInput.value = "";

        fileNameDisplay.textContent =
            "📁 No file selected";

        selectedFileName.textContent =
            "No file selected";

        fileHashResult.value = "";

        fileHashMessage.textContent = "";

        fileHashMessage.className =
            "crypto-message";

    }
);


// Copy

fileHashCopyButton.addEventListener(
    "click",
    async function () {

        if (!fileHashResult.value) {

            showFileHashMessage(
                "There is no hash to copy.",
                "error"
            );

            return;
        }


        await navigator.clipboard.writeText(
            fileHashResult.value
        );


        showFileHashMessage(
            "File hash copied to clipboard.",
            "success"
        );

    }
);

// ==========================================
// AUTHENTICATION
// ==========================================

const registerUsername =
    document.getElementById("register-username");

const registerPassword =
    document.getElementById("register-password");

const registerButton =
    document.getElementById("register-button");

const registerClearButton =
    document.getElementById("register-clear");

const registerMessage =
    document.getElementById("register-message");


const loginUsername =
    document.getElementById("login-username");

const loginPassword =
    document.getElementById("login-password");

const loginButton =
    document.getElementById("login-button");

const loginClearButton =
    document.getElementById("login-clear");

const loginMessage =
    document.getElementById("login-message");


// ==========================================
// AUTHENTICATION MESSAGES
// ==========================================

function showRegisterMessage(message, type) {

    registerMessage.textContent = message;
    registerMessage.className = "auth-message";
    registerMessage.classList.add(type);

}


function showLoginMessage(message, type) {

    loginMessage.textContent = message;
    loginMessage.className = "auth-message";
    loginMessage.classList.add(type);

}


// ==========================================
// REGISTER USER
// ==========================================

async function registerUser() {

    const username = registerUsername.value.trim();
    const password = registerPassword.value;

    registerMessage.textContent = "";
    registerMessage.className = "auth-message";


    if (!username) {

        showRegisterMessage(
            "Please enter a username.",
            "error"
        );

        return;
    }


    if (!password) {

        showRegisterMessage(
            "Please enter a password.",
            "error"
        );

        return;
    }


    try {

        const response = await fetch(
            "/api/auth/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            showRegisterMessage(
                data.message || data.error,
                "error"
            );

            return;
        }


        showRegisterMessage(
            "User registered successfully.",
            "success"
        );


        registerPassword.value = "";


    } catch (error) {

        console.error(error);

        showRegisterMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    }

}


// ==========================================
// LOGIN USER
// ==========================================

async function loginUser() {

    const username = loginUsername.value.trim();
    const password = loginPassword.value;

    loginMessage.textContent = "";
    loginMessage.className = "auth-message";


    if (!username) {

        showLoginMessage(
            "Please enter a username.",
            "error"
        );

        return;
    }


    if (!password) {

        showLoginMessage(
            "Please enter a password.",
            "error"
        );

        return;
    }


    openCaptchaModal();
}

async function performLogin() {

    const username = loginUsername.value.trim();
    const password = loginPassword.value;


    try {

        const response = await fetch(
            "/api/auth/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            showLoginMessage(
                data.message || data.error,
                "error"
            );

            return;
        }


        // Store the session token returned by the server
        currentSessionToken = data.session_token;

        // Update the session UI
        checkCurrentSession();

        showLoginMessage(
            "Login successful.",
            "success"
        );

        loginPassword.value = "";

    } catch (error) {

        console.error(error);

        showLoginMessage(
            "Unable to connect to the WatchByte server.",
            "error"
        );

    }

}


// ==========================================
// REGISTER BUTTON
// ==========================================

registerButton.addEventListener(
    "click",
    () => {

        registerUser();

    }
);


// ==========================================
// LOGIN BUTTON
// ==========================================

loginButton.addEventListener(
    "click",
    () => {

        loginUser();

    }
);


// ==========================================
// CLEAR REGISTER
// ==========================================

registerClearButton.addEventListener(
    "click",
    () => {

        registerUsername.value = "";
        registerPassword.value = "";

        registerMessage.textContent = "";
        registerMessage.className = "auth-message";

    }
);


// ==========================================
// CLEAR LOGIN
// ==========================================

loginClearButton.addEventListener(
    "click",
    () => {

        loginUsername.value = "";
        loginPassword.value = "";

        loginMessage.textContent = "";
        loginMessage.className = "auth-message";

    }
);

/* ==========================================
   FIREWALL & IDS NETWORK ANALYSIS
   ========================================== */

const networkAnalyzeBtn = document.getElementById("network-analyze");
const networkClearBtn = document.getElementById("network-clear");

const networkSourceIp = document.getElementById("network-source-ip");
const networkPort = document.getElementById("network-port");
const networkProtocol = document.getElementById("network-protocol");
const networkAttempts = document.getElementById("network-attempts");

const networkMessage = document.getElementById("network-message");

const networkFinalAction = document.getElementById("network-final-action");

const networkFirewallAction =
    document.getElementById("network-firewall-action");

const networkFirewallReason =
    document.getElementById("network-firewall-reason");

const networkIdsStatus =
    document.getElementById("network-ids-status");

const networkIdsAlerts =
    document.getElementById("network-ids-alerts");


/* ==========================================
   ANALYZE NETWORK TRAFFIC
========================================== */

if (networkAnalyzeBtn) {

    networkAnalyzeBtn.addEventListener("click", async function () {

        const sourceIp = networkSourceIp.value.trim();
        const port = networkPort.value.trim();
        const protocol = networkProtocol.value;
        const attempts = networkAttempts.value.trim();


        /* Validation */

        if (!sourceIp || !port || !protocol || !attempts) {

            networkMessage.textContent =
                "Please fill in all network fields.";

            networkMessage.className =
                "network-message error";

            return;
        }


        networkMessage.textContent =
            "Analyzing network traffic...";

        networkMessage.className =
            "network-message";


        try {

            const response = await fetch(
                "/api/network/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        source_ip: sourceIp,
                        destination_port: Number(port),
                        protocol: protocol,
                        connection_attempts: Number(attempts)
                    })
                }
            );


            const data = await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.error || "Network analysis failed."
                );
            }


            const result = data.result;


            /* ==========================================
               FINAL DECISION
            ========================================== */

            networkFinalAction.textContent =
                result.final_action;

            networkFinalAction.className = "";

            if (result.final_action === "ALLOW") {

                networkFinalAction.classList.add("allow");

            } else if (result.final_action === "BLOCK") {

                networkFinalAction.classList.add("block");

            } else if (result.final_action === "ALERT") {

                networkFinalAction.classList.add("alert");

            }


            /* ==========================================
               FIREWALL RESULT
            ========================================== */

            
            networkFirewallAction.textContent =
                result.firewall.action;

            networkFirewallAction.className = "";

            if (result.firewall.action === "ALLOW") {

                networkFirewallAction.classList.add("allow");

            } else {

                networkFirewallAction.classList.add("block");

            }

            networkFirewallReason.textContent =
                result.firewall.reason;


            /* ==========================================
               IDS RESULT
            ========================================== */

            if (result.ids.alert) {

                networkIdsStatus.textContent =
                    "⚠️ Suspicious activity detected.";

                networkIdsStatus.className =
                    "alert";

                networkIdsAlerts.textContent =
                    result.ids.alerts.join(" ");

            } else {

                networkIdsStatus.textContent =
                    "✓ No suspicious activity detected.";

                networkIdsStatus.className =
                    "allow";

                networkIdsAlerts.textContent =
                    "No IDS alerts generated.";

            }


            networkMessage.textContent =
                "Network analysis completed successfully.";

            networkMessage.className =
                "network-message success";


        } catch (error) {

            networkMessage.textContent =
                error.message;

            networkMessage.className =
                "network-message error";

        }

    });

}


/* ==========================================
   CLEAR NETWORK FORM
========================================== */

if (networkClearBtn) {

    networkClearBtn.addEventListener("click", function () {

        networkSourceIp.value = "";
        networkPort.value = "";
        networkProtocol.value = "tcp";
        networkAttempts.value = "";

        networkMessage.textContent = "";
        networkMessage.className = "network-message";


        networkFinalAction.textContent =
            "Awaiting analysis...";

        networkFinalAction.className = "";


        networkFirewallAction.textContent =
            "No analysis performed.";

        networkIdsStatus.className = "";

        networkFirewallAction.className = "";

        networkFirewallReason.textContent =
            "Firewall result will appear here.";


        networkIdsStatus.textContent =
            "No analysis performed.";

        networkIdsAlerts.textContent =
            "IDS alerts will appear here.";

    });

}

/* ==========================================
   SECURITY LOGS
   ========================================== */

const logsList = document.getElementById("logs-list");
const logsMessage = document.getElementById("logs-message");
const logsRefresh = document.getElementById("logs-refresh");
const logsClear = document.getElementById("logs-clear");


function showLogsMessage(message, type) {

    logsMessage.textContent = message;
    logsMessage.className = `logs-message ${type}`;

}


function renderLogs(logs) {

    logsList.innerHTML = "";

    if (!logs || logs.length === 0) {

        logsList.innerHTML = `
            <div class="logs-empty">

                <strong>No security events</strong>

                <p>
                    Security events will appear here.
                </p>

            </div>
        `;

        return;
    }


    logs.forEach(function(log) {

        const logEntry = document.createElement("div");

        logEntry.className = "log-entry";


        const level = String(log.level || "").toLowerCase();


        logEntry.innerHTML = `

            <span class="log-timestamp">
                ${log.timestamp}
            </span>

            <span class="log-level ${level}">
                ${log.level}
            </span>

            <span class="log-event">
                ${log.event}
            </span>

            <span class="log-source">
                ${log.source}
            </span>

        `;


        logsList.appendChild(logEntry);

    });

}


async function loadSecurityLogs() {

    try {

        const response = await fetch("/api/logs", {
            headers: {
                "Authorization": "Bearer " + currentSessionToken
            }
        });

        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Unable to load security logs."
            );

        }


        renderLogs(data.logs);

        showLogsMessage(
            `${data.logs.length} security event(s) loaded.`,
            "success"
        );

    }

    catch (error) {

        console.error("Security Logs Error:", error);

        showLogsMessage(
            "Unable to load security logs.",
            "error"
        );

    }

}


async function clearSecurityLogs() {

    try {

        const response = await fetch(
            "/api/logs/clear",
            {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + currentSessionToken
                }
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error || "Unable to clear security logs."
            );

        }


        renderLogs([]);

        showLogsMessage(
            "Security logs cleared successfully.",
            "success"
        );

    }

    catch (error) {

        console.error("Security Logs Error:", error);

        showLogsMessage(
            "Unable to clear security logs.",
            "error"
        );

    }

}


/* Refresh button */

if (logsRefresh) {

    logsRefresh.addEventListener(
        "click",
        loadSecurityLogs
    );

}


/* Clear button */

if (logsClear) {

    logsClear.addEventListener(
        "click",
        clearSecurityLogs
    );

}

/* ==========================================
   CAPTCHA VERIFICATION
========================================== */

const captchaModal =
    document.getElementById("captcha-modal");

const captchaText =
    document.getElementById("captcha-text");

const captchaInput =
    document.getElementById("captcha-input");

const captchaMessage =
    document.getElementById("captcha-message");

const captchaRefresh =
    document.getElementById("captcha-refresh");

const captchaVerify =
    document.getElementById("captcha-verify");

const captchaClose =
    document.getElementById("captcha-close");

const captchaCancel =
    document.getElementById("captcha-cancel");


let currentCaptcha = "";
let currentCaptchaChallenge = "";

/* ==========================================
   OPEN CAPTCHA
========================================== */

async function openCaptchaModal() {

    captchaModal.style.display = "flex";

    captchaInput.value = "";

    captchaMessage.textContent = "";

    captchaMessage.className =
        "captcha-message";

    await generateCaptchaForLogin();

    captchaInput.focus();

}


/* ==========================================
   CLOSE CAPTCHA
========================================== */

function closeCaptchaModal() {

    captchaModal.style.display = "none";

    captchaInput.value = "";

    captchaMessage.textContent = "";

    captchaMessage.className =
        "captcha-message";

}


/* ==========================================
   GENERATE CAPTCHA
========================================== */

async function generateCaptchaForLogin() {

    captchaText.textContent = "Loading...";

    try {

        const response = await fetch(
            "/api/captcha/generate"
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Unable to generate CAPTCHA."
            );

        }


        currentCaptchaChallenge = data.challenge_id;
        currentCaptcha = data.captcha;

        captchaText.textContent =
            currentCaptcha;


    } catch (error) {

        console.error(error);

        captchaText.textContent =
            "ERROR";

        captchaMessage.textContent =
            "Unable to generate CAPTCHA.";

        captchaMessage.className =
            "captcha-message error";

    }

}


/* ==========================================
   VERIFY CAPTCHA
========================================== */

async function verifyCaptchaForLogin() {

    const submittedCaptcha =
        captchaInput.value.trim();


    captchaMessage.textContent = "";

    captchaMessage.className =
        "captcha-message";


    if (!submittedCaptcha) {

        captchaMessage.textContent =
            "Please enter the CAPTCHA.";

        captchaMessage.className =
            "captcha-message error";

        return;

    }


    captchaVerify.disabled = true;

    captchaVerify.textContent =
        "Verifying...";


    try {

        const response = await fetch(
            "/api/captcha/verify",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    challenge_id: currentCaptchaChallenge,
                    submitted: submittedCaptcha
                })
            }
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "CAPTCHA verification failed."
            );

        }


        if (!data.verified) {

            captchaMessage.textContent =
                "Incorrect CAPTCHA. Please try again.";

            captchaMessage.className =
                "captcha-message error";

            captchaInput.value = "";

            await generateCaptchaForLogin();

            captchaInput.focus();

            return;

        }


        captchaMessage.textContent =
            "CAPTCHA verified successfully.";

        captchaMessage.className =
            "captcha-message success";


        /*
         * CAPTCHA passed.
         * Now continue with login.
         */

        closeCaptchaModal();

        await performLogin();


    } catch (error) {

        console.error(error);

        captchaMessage.textContent =
            "Unable to verify CAPTCHA.";

        captchaMessage.className =
            "captcha-message error";

    } finally {

        captchaVerify.disabled = false;

        captchaVerify.textContent =
            "Verify CAPTCHA";

    }

}


/* ==========================================
   CAPTCHA BUTTONS
========================================== */

if (captchaRefresh) {

    captchaRefresh.addEventListener(
        "click",
        generateCaptchaForLogin
    );

}


if (captchaVerify) {

    captchaVerify.addEventListener(
        "click",
        verifyCaptchaForLogin
    );

}


if (captchaClose) {

    captchaClose.addEventListener(
        "click",
        closeCaptchaModal
    );

}


if (captchaCancel) {

    captchaCancel.addEventListener(
        "click",
        closeCaptchaModal
    );

}

// ==========================================
// CSRF TOKEN
// ==========================================

let currentCsrfToken = null;


async function fetchCsrfToken() {
    const response = await fetch("/api/security/csrf", {
        method: "GET"
    });

    const data = await response.json();

    if (!response.ok || !data.success || !data.csrf_token) {
        throw new Error("Unable to obtain CSRF token.");
    }

    currentCsrfToken = data.csrf_token;

    return currentCsrfToken;
}

// ==========================================
// SESSION MANAGEMENT
// ==========================================

let currentSessionToken = null;


const sessionIndicator = document.getElementById("session-indicator");
const sessionStatusMessage = document.getElementById("session-status-message");
const sessionUser = document.getElementById("session-user");
const sessionLogout = document.getElementById("session-logout");


function updateSessionUI(active, username = "") {

    if (active) {

        sessionIndicator.textContent = "ACTIVE";
        sessionIndicator.classList.remove("inactive");
        sessionIndicator.classList.add("active");

        sessionStatusMessage.textContent =
            "Your WatchByte session is active.";

        sessionUser.textContent =
            "User: " + username;

        sessionLogout.disabled = false;

    } else {

        sessionIndicator.textContent = "INACTIVE";
        sessionIndicator.classList.remove("active");
        sessionIndicator.classList.add("inactive");

        sessionStatusMessage.textContent =
            "No active session.";

        sessionUser.textContent =
            "Not logged in";

        sessionLogout.disabled = true;
    }
}


// ==========================================
// CHECK CURRENT SESSION
// ==========================================

async function checkCurrentSession() {

    if (!currentSessionToken) {
        updateSessionUI(false);
        return;
    }

    try {

        const response = await fetch("/api/auth/session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_token: currentSessionToken
            })
        });

        const data = await response.json();


        if (data.success && data.valid) {

            updateSessionUI(true, data.username);

        } else {

            currentSessionToken = null;
            updateSessionUI(false);
        }

    } catch (error) {

        console.error("Session check failed:", error);
        updateSessionUI(false);
    }
}


// ==========================================
// LOGOUT
// ==========================================

sessionLogout.addEventListener("click", async function() {

    if (!currentSessionToken) {
        return;
    }


    try {

        const csrfToken = await fetchCsrfToken();

        const response = await fetch("/api/auth/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-Token": csrfToken
            },
            body: JSON.stringify({
                session_token: currentSessionToken,
                csrf_token: csrfToken
            })
        });


        const data = await response.json();


        if (data.success) { 

            currentSessionToken = null;

            updateSessionUI(false);

            console.log("Logout successful.");

        } else {

            console.error(data.message || "Logout failed.");
        }


    } catch (error) {

        console.error("Logout error:", error);
    }

});


// Initial session state
updateSessionUI(false);