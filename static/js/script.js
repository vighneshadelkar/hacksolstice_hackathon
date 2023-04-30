let add_btn=document.getElementById("add-btn");

add_btn.addEventListener('click',(e)=>{
    e.preventDefault();
    let input = document.getElementById("main-input").value;
    //ul  
    let ul = document.getElementById("lists");

    // li_div in which li and button is present
    let li_div = document.createElement("li_div");
    li_div.setAttribute("id", "li_div");

    // li elemnt created
    let li = document.createElement("li");
    li.classList.add("list");
    let liinput = document.createTextNode(input);

    // delete button
    let del = document.createElement("button");
    del.classList.add("del-btn");
    let delval=document.createTextNode("DELETE");

    // add child to li_div
    del.appendChild(delval);
    li.appendChild(liinput);
    li_div.appendChild(li);
    li_div.appendChild(del);

    localStorage.setItem("data", JSON.stringify(input));
    JSON.parse(localStorage.getItem("data"));
    if (input == "") {
        alert("PLEASE ENTER A TASK");
    }
    else {
        ul.appendChild(li_div);
        let input = document.getElementById("main-input").value;
        document.getElementById("main-input").value = "";
    }
    del.addEventListener('click',()=>{
        ul.removeChild(li_div);
        li_div.removeChild(del);
    });
});