document.getElementById("delete-button").addEventListener("click",deleteUser);

async function  deleteUser()
{

  const user_id = document.getElementById("delete-button").value;
  const res = await axios.delete('/delete/', { data: { user_id: user_id } });
  console.log(res.data)
  if(res.data =="Success")
  {
    alert("User has been deleted")
    window.location.href = "http://127.0.0.1:3000/";
  }
  else
  {
    alert("there was a problem deleting the user")
    window.location.href = "http://127.0.0.1:3000/";
  }
}