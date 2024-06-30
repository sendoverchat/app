function deletePopup() {
    document.querySelectorAll(".popup").forEach((node) => {
        node.remove();
    })
}
class Popup
{

    constructor(title, paragraphe, input_placeholder, input_type, input_id, button_name, button_id){
        this.title = title;
        this.paragraphe = paragraphe;
        this.input_placeholder = input_placeholder;
        this.input_type = input_type;
        this.input_id = input_id;
        this.button_name = button_name;
        this.button_id = button_id;
    }

    display() {

        const popup = document.body.innerHTML += (`
            <div class="popup">
                <svg class="close-btn" onclick="deletePopup()" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M18 6L6 18M6 6L18 18"  stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h1>${this.title}</h1>
                <p>${this.paragraphe}</p>
                <input type="${this.input_type}" name="Input" id="${this.input_id}" placeholder="${this.input_placeholder}">
                <button class="default" id="${this.button_id}">${this.button_name}</button>
            </div>
        `);

    }
}
