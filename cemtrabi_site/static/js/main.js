// Remove o pop-up automaticamente após 4 segundos
document.addEventListener("DOMContentLoaded", function () {
    const toast = document.getElementById("toast-success");

    if (toast) {
        setTimeout(() => {
            toast.remove();
        }, 4000);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".slide");
    const prev = document.querySelector(".slider-btn.prev");
    const next = document.querySelector(".slider-btn.next");

    if (!slides.length || !prev || !next) {
        return;
    }

    let index = 0;
    let interval;

    function showSlide(i) {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[i].classList.add("active");
    }

    function nextSlide() {
        index = (index === slides.length - 1) ? 0 : index + 1;
        showSlide(index);
    }

    function prevSlide() {
        index = (index === 0) ? slides.length - 1 : index - 1;
        showSlide(index);
    }

    // AUTO SLIDE (4 SEGUNDOS)
    function startAutoSlide() {
        interval = setInterval(nextSlide, 4000);
    }

    function resetAutoSlide() {
        clearInterval(interval);
        startAutoSlide();
    }

    // Eventos das setas
    next.addEventListener("click", function () {
        nextSlide();
        resetAutoSlide();
    });

    prev.addEventListener("click", function () {
        prevSlide();
        resetAutoSlide();
    });

    // Inicia
    showSlide(index);
    startAutoSlide();
});

document.addEventListener("DOMContentLoaded", function () {
    const accordionHeaders = document.querySelectorAll(".accordion-header");

    accordionHeaders.forEach(header => {
        header.addEventListener("click", function () {
            const item = this.parentElement;

            // Fecha os outros
            document.querySelectorAll(".accordion-item").forEach(i => {
                if (i !== item) {
                    i.classList.remove("active");
                }
            });

            // Abre / fecha o atual
            item.classList.toggle("active");
        });
    });
});

// ===============================
// MÁSCARA DE CNPJ
// ===============================
document.addEventListener("DOMContentLoaded", function () {
    const cnpjInput = document.querySelector("input[name='cnpj']");

    if (cnpjInput) {
        cnpjInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\D/g, "");

            value = value.replace(/^(\d{2})(\d)/, "$1.$2");
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})(\d)/, ".$1/$2");
            value = value.replace(/(\d{4})(\d)/, "$1-$2");

            e.target.value = value.substring(0, 18);
        });
    }
});

// ===============================
// MÁSCARA DE TELEFONE
// ===============================
document.addEventListener("DOMContentLoaded", function () {
    const cpfInput = document.querySelector("input[name='cpf']");

    if (cpfInput) {
        cpfInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\D/g, "");

            value = value.replace(/^(\d{3})(\d)/, "$1.$2");
            value = value.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})(\d)/, ".$1-$2");

            e.target.value = value.substring(0, 14);
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const rgInput = document.querySelector("input[name='rg']");

    if (rgInput) {
        rgInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/[^0-9xX]/g, "").toUpperCase();

            value = value.replace(/^(\d{2})(\d)/, "$1.$2");
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})([0-9X])/, ".$1-$2");

            e.target.value = value.substring(0, 12);
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const phoneInput = document.querySelector("input[name='telefone']");

    if (phoneInput) {
        phoneInput.addEventListener("input", function (e) {
            let value = e.target.value.replace(/\D/g, "");

            if (value.length <= 10) {
                value = value.replace(/^(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{4})(\d)/, "$1-$2");
            } else {
                value = value.replace(/^(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{5})(\d)/, "$1-$2");
            }

            e.target.value = value.substring(0, 15);
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('submit-btn');
    const form = button ? button.closest('form') : null;
    let loadingTimeout;

    function setButtonLoading(isLoading) {
        if (!button) {
            return;
        }

        const buttonText = button.querySelector('.btn-text');
        const buttonLoading = button.querySelector('.btn-loading');

        button.classList.toggle('loading', isLoading);
        button.disabled = isLoading;

        if (buttonText) {
            buttonText.style.display = isLoading ? 'none' : 'inline';
        }

        if (buttonLoading) {
            buttonLoading.style.display = isLoading ? 'inline-flex' : 'none';
        }
    }

    function showSubmitMessage(message) {
        if (!form || document.querySelector('.submit-feedback')) {
            return;
        }

        const feedback = document.createElement('div');
        feedback.className = 'toast error submit-feedback';
        feedback.textContent = message;
        document.body.appendChild(feedback);

        setTimeout(() => {
            feedback.remove();
        }, 5000);
    }

    function resetSubmitState() {
        if (form) {
            form.dataset.submitting = 'false';
        }
        clearTimeout(loadingTimeout);
        setButtonLoading(false);
    }

    if (form) {
        resetSubmitState();

        form.addEventListener('submit', function (event) {
            if (form.dataset.submitting === 'true') {
                event.preventDefault();
                return;
            }

            form.dataset.submitting = 'true';
            setButtonLoading(true);

            loadingTimeout = setTimeout(() => {
                resetSubmitState();
                showSubmitMessage(
                    'O envio está demorando mais que o esperado. Verifique sua conexão e tente novamente.'
                );
            }, 45000);
        });

        window.addEventListener('pageshow', resetSubmitState);
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById("hamburger");
    const menu = document.getElementById("menu");
    const overlay = document.getElementById("overlay");

    if (hamburger && menu && overlay) {
        const menuLinks = menu.querySelectorAll("a");

        const syncMenuState = (isActive) => {
            menu.classList.toggle("active", isActive);
            overlay.classList.toggle("active", isActive);
            hamburger.setAttribute("aria-expanded", String(isActive));
        };

        hamburger.addEventListener("click", () => {
            syncMenuState(!menu.classList.contains("active"));
        });

        overlay.addEventListener("click", () => {
            syncMenuState(false);
        });

        menuLinks.forEach((link) => {
            link.addEventListener("click", () => {
                syncMenuState(false);
            });
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                syncMenuState(false);
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("encaminhamento-success-modal");
    const closeButton = document.querySelector("[data-close-success-modal]");

    if (modal && closeButton) {
        closeButton.addEventListener("click", function () {
            modal.remove();
        });
    }
});
