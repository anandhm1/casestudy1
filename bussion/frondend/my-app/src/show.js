import { useEffect, useState } from 'react';
import axios from "axios";
import { useParams } from 'react-router-dom';
import "../node_modules/bootstrap/dist/css/bootstrap.min.css"
import fileDownload from 'js-file-download'


const handleDownload = (url, filename) => {
  axios.get(url, {
    responseType: 'blob',
  })
  .then((res) => {
    fileDownload(res.data, filename)
  })
}

const Shows=()=>{
  const {id}=useParams('id')
  console.log(id)
    const [books,setBook]=useState([])
    const [books1,setBook1,]=useState()
    useEffect(()=>{
      async function getAllStudent(){
        try{
          const books = await axios.get("http://127.0.0.1:8000/company/std/"+id+"/")
          console.log(books.data.file)
          setBook(books.data.data1)
          setBook1(books.data.file)
        }
        catch (error){console.log(error)}
      }
      getAllStudent()
    },[])
    return (
      <div className='container-fluid' >
        <header >
         <table className="table">
           <tr id='row'>
             <th>Name</th>
             <th>Currency</th>
             <th>Amount</th>
             <th>Transaction Data</th>
             <th>converted Currency</th>
             <th>Currency Amount</th>
           </tr>

           {books.map((book,i) =>{
             return <>
             <tr>
               <td>{book.name}</td>
               <td>{book.currency_name}</td>
               <td>{book.amount}</td>
               <td>{book.Date}</td>
               <td>{book.converted_currency}</td>
               <td>{book.converted_amount}</td>
             </tr>

             </>
           })
           }

         </table>
         <button onClick={() => {handleDownload(books1, 'test-download.csv')
}}>Download File</button>
        </header>
      </div>
    );
};

export default Shows;