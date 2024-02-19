
document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        var e_ = document.getElementById("searchID").value
        if(e_ != ""){
            location.href = "/region/" + e_
            }
        }
})