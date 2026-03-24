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
    const form = document.querySelector('form');
    const button = document.getElementById('submit-btn');

    if (form && button) {
        form.addEventListener('submit', function () {
            button.classList.add('loading');

            button.querySelector('.btn-text').style.display = 'none';
            button.querySelector('.btn-loading').style.display = 'inline';
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.getElementById("hamburger")
    const menu = document.getElementById("menu")
    const overlay = document.getElementById("overlay")

    if (hamburger && menu && overlay) {
        hamburger.addEventListener("click", () => {
            menu.classList.toggle("active")
            overlay.classList.toggle("active")
        })

        overlay.addEventListener("click", () => {
            menu.classList.remove("active")
            overlay.classList.remove("active")
        })
    }
})

