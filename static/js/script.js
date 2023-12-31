window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const deleteBtns = document.querySelectorAll(".delete-button");
for (let i = 0; i < deleteBtns.length; i++) {
  const btn = deleteBtns[i];
  btn.onclick = async function (e) {
    const _id = e.target.dataset["id"];
    const _url = e.target.dataset["url"]
    let response = await fetch(`/${_url}/${_id}`, {
      method: "DELETE",
    });
    if (response.ok) {
      window.location.href = "/";
    } else {
      alert('A server error occurred. Please retry.');
      console.log(response); 
    }
  };
}

