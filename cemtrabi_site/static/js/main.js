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

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("[data-encaminhamento-form]");
    const list = document.querySelector("[data-colaboradores-list]");
    const template = document.getElementById("colaborador-empty-form");
    const addButton = document.querySelector("[data-add-colaborador]");
    const totalForms = document.getElementById("id_colaboradores-TOTAL_FORMS");

    if (!form || !list || !template || !addButton || !totalForms) {
        return;
    }

    function getActiveCards() {
        return Array.from(list.querySelectorAll("[data-colaborador-form]"))
            .filter(card => card.dataset.deleted !== "true");
    }

    function setInputDisabled(scope, disabled) {
        scope.querySelectorAll("input, select, textarea").forEach(input => {
            if (!input.name.endsWith("-DELETE")) {
                input.disabled = disabled;
            }
        });
    }

    function isCardEmpty(card) {
        return Array.from(card.querySelectorAll("input, select, textarea"))
            .filter(input => !input.name.endsWith("-DELETE"))
            .filter(input => !input.name.endsWith("-copiar_de_indice"))
            .filter(input => !input.name.endsWith("-tipo_exame"))
            .filter(input => !input.matches("[data-copy-source]"))
            .filter(input => input.type !== "hidden")
            .every(input => {
                if (input.type === "checkbox" || input.type === "radio") {
                    return !input.checked;
                }

                if (input.type === "file") {
                    return !input.files || input.files.length === 0;
                }

                return !String(input.value || "").trim();
            });
    }

    function getField(card, suffix) {
        return card.querySelector(`[name$='-${suffix}']`);
    }

    function getFormIndex(card) {
        const field = card.querySelector("[name^='colaboradores-']");
        const match = field ? field.name.match(/^colaboradores-(\d+)-/) : null;
        return match ? Number(match[1]) : null;
    }

    function getCopySourceCard(targetCard) {
        const referenceField = getField(targetCard, "copiar_de_indice");

        if (!referenceField || referenceField.value === "") {
            return null;
        }

        const referenceIndex = Number(referenceField.value);

        return getActiveCards().find(card => getFormIndex(card) === referenceIndex) || null;
    }

    function getCollaboratorOptionLabel(card, position) {
        const role = getField(card, "funcao")?.value.trim();
        const name = getField(card, "nome")?.value.trim();
        const identity = role || name || "Dados ainda não identificados";
        const complement = role && name ? ` · ${name}` : "";
        return `Colaborador ${position + 1} · ${identity}${complement}`;
    }

    function updateCopySourceOptions() {
        const activeCards = getActiveCards();

        activeCards.forEach((card, position) => {
            const select = card.querySelector("[data-copy-source]");
            const referenceField = getField(card, "copiar_de_indice");

            if (!select || !referenceField) {
                return;
            }

            const selectedValue = referenceField.value;
            select.replaceChildren(new Option("Selecione um colaborador já preenchido", ""));

            activeCards.slice(0, position).forEach((sourceCard, sourcePosition) => {
                const sourceIndex = getFormIndex(sourceCard);

                if (sourceIndex !== null) {
                    select.add(new Option(
                        getCollaboratorOptionLabel(sourceCard, sourcePosition),
                        String(sourceIndex)
                    ));
                }
            });

            const selectedStillExists = Array.from(select.options)
                .some(option => option.value === selectedValue);

            select.value = selectedStillExists ? selectedValue : "";
            referenceField.value = select.value;
        });
    }

    function copyExams(sourceCard, targetCard) {
        if (!sourceCard || sourceCard === targetCard) {
            return;
        }

        const examSuffixes = [
            "exame_clinico",
            "audiometria",
            "acuidade_visual",
            "eletrocardiograma",
            "eletroencefalograma",
            "espirometria",
            "avaliacao_psicossocial",
            "raio_x_torax",
            "teste_romberg",
            "hemograma",
            "glicemia",
            "acido_hipurico",
            "acido_metil_hipurico",
            "grupo_sanguineo_fator_rh",
            "outro_exame"
        ];

        examSuffixes.forEach(suffix => {
            const source = getField(sourceCard, suffix);
            const target = getField(targetCard, suffix);

            if (source && target) {
                target.checked = source.checked;
            }
        });

        const sourceDescription = getField(sourceCard, "descricao_outro_exame");
        const targetDescription = getField(targetCard, "descricao_outro_exame");

        if (sourceDescription && targetDescription) {
            targetDescription.value = sourceDescription.value;
        }
    }

    function copyProfessionalData(sourceCard, targetCard) {
        if (!sourceCard || sourceCard === targetCard) {
            return;
        }

        [
            "funcao",
            "setor",
            "data_admissao",
            "tipo_exame",
            "riscos_ocupacionais"
        ].forEach(suffix => {
            const source = getField(sourceCard, suffix);
            const target = getField(targetCard, suffix);

            if (source && target) {
                target.value = source.value;
            }
        });

        copyExams(sourceCard, targetCard);
    }

    function syncPcmsoUpload(card) {
        const toggle = getField(card, "anexar_pcmso");
        const uploadArea = card.querySelector("[data-pcmso-upload]");
        const fileInput = getField(card, "pcmso");

        if (!toggle || !uploadArea) {
            return;
        }

        const shouldShow = toggle.checked;
        uploadArea.hidden = !shouldShow;

        if (fileInput) {
            fileInput.disabled = !shouldShow;

            if (!shouldShow) {
                fileInput.value = "";
            }
        }
    }

    function updateCollaboratorUi() {
        const activeCards = getActiveCards();

        activeCards.forEach((card, index) => {
            const label = card.querySelector(".colaborador-card-header .eyebrow");
            if (label) {
                label.textContent = `Colaborador ${index + 1}`;
            }

            const cloneOptions = card.querySelector("[data-clone-options]");
            if (cloneOptions) {
                cloneOptions.hidden = index === 0;
                setInputDisabled(cloneOptions, index === 0);
            }

            syncPcmsoUpload(card);
        });

        updateCopySourceOptions();

        list.querySelectorAll("[data-remove-colaborador]").forEach(button => {
            button.hidden = activeCards.length <= 1;
        });
    }

    function addCollaborator() {
        const index = Number(totalForms.value);
        const html = template.innerHTML
            .replace(/__prefix__/g, index)
            .replace(/__prefix_num__/g, index + 1);

        list.insertAdjacentHTML("beforeend", html);
        totalForms.value = index + 1;

        updateCollaboratorUi();
    }

    addButton.addEventListener("click", function () {
        addCollaborator();
    });

    list.addEventListener("click", function (event) {
        const removeButton = event.target.closest("[data-remove-colaborador]");

        if (!removeButton) {
            return;
        }

        const activeCards = getActiveCards();
        if (activeCards.length <= 1) {
            return;
        }

        const card = removeButton.closest("[data-colaborador-form]");
        const deleteInput = card.querySelector("input[name$='-DELETE']");

        if (deleteInput) {
            deleteInput.value = "on";
            deleteInput.checked = true;
        }

        card.dataset.deleted = "true";
        card.hidden = true;
        updateCollaboratorUi();
    });

    list.addEventListener("change", function (event) {
        const input = event.target;
        const card = input.closest("[data-colaborador-form]");

        if (!card) {
            return;
        }

        if (input.matches("[data-copy-source]")) {
            const referenceField = getField(card, "copiar_de_indice");

            if (referenceField) {
                referenceField.value = input.value;
            }

            const sourceCard = getCopySourceCard(card);

            if (sourceCard) {
                copyProfessionalData(sourceCard, card);
            }

            updateCopySourceOptions();
            return;
        }

        if (input.name.endsWith("-anexar_pcmso")) {
            syncPcmsoUpload(card);
        }
    });

    form.addEventListener("input", function (event) {
        const input = event.target;

        if (!(input instanceof HTMLInputElement)) {
            return;
        }

        const name = input.name || "";
        let value = input.value.replace(/\D/g, "");

        if (name === "cnpj") {
            value = value.replace(/^(\d{2})(\d)/, "$1.$2");
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})(\d)/, ".$1/$2");
            value = value.replace(/(\d{4})(\d)/, "$1-$2");
            input.value = value.substring(0, 18);
        }

        if (name.endsWith("-cpf")) {
            value = value.replace(/^(\d{3})(\d)/, "$1.$2");
            value = value.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})(\d)/, ".$1-$2");
            input.value = value.substring(0, 14);
        }

        if (name.endsWith("-rg")) {
            value = input.value.replace(/[^0-9xX]/g, "").toUpperCase();
            value = value.replace(/^(\d{2})(\d)/, "$1.$2");
            value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
            value = value.replace(/\.(\d{3})([0-9X])/, ".$1-$2");
            input.value = value.substring(0, 12);
        }

        if (name === "telefone") {
            if (value.length <= 10) {
                value = value.replace(/^(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{4})(\d)/, "$1-$2");
            } else {
                value = value.replace(/^(\d{2})(\d)/, "($1) $2");
                value = value.replace(/(\d{5})(\d)/, "$1-$2");
            }

            input.value = value.substring(0, 15);
        }

        if (name.endsWith("-funcao") || name.endsWith("-nome")) {
            updateCopySourceOptions();
        }
    });

    form.addEventListener("submit", function () {
        getActiveCards().forEach((card, index) => {
            if (index > 0 && isCardEmpty(card)) {
                const deleteInput = card.querySelector("input[name$='-DELETE']");

                if (deleteInput) {
                    deleteInput.value = "on";
                    deleteInput.checked = true;
                }

                card.dataset.deleted = "true";
            }
        });

        updateCollaboratorUi();
    });

    updateCollaboratorUi();
});
