function loadEditBox(clicked_id){
        /*alert(clicked_id);*/
        document.getElementById("postID").value = clicked_id;
        document.getElementById("editPostSubject").value = document.getElementById("postSubject"+clicked_id).innerHTML
        document.getElementById("editPostTime").innerHTML = document.getElementById("postTime"+clicked_id).innerHTML 
        document.getElementById("editPostMessage").value = document.getElementById("postMessage"+clicked_id).innerHTML
        document.getElementById("editPostSubject").disabled = false;
        document.getElementById("editPostMessage").disabled = false;
        document.getElementById("myFile").disabled = false;
        document.getElementById("editConfirmBtn").disabled = false;

        if (document.getElementById("postImg" + clicked_id).src != "NA") {
            document.getElementById("editPostImg").src = document.getElementById("postImg" + clicked_id).src
            document.getElementById("postImgSrc").value = document.getElementById("postImg" + clicked_id).src
            document.getElementById("editPostImg").style.visibility = 'visible'
        } 

        if (document.getElementById("postImg" + clicked_id).src.slice(-2) == "NA"){
            document.getElementById("editPostImg").style.visibility = 'hidden'
            document.getElementById("editPostImg").src = ""
            document.getElementById("postImgSrc").value = ""
            
        }
    }