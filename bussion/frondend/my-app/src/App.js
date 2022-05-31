import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import axios from "axios";
import {Route,Routes} from "react-router-dom";
import Shows from './show';
import AddStudent from './uploadfile';



const MyApp=()=>{
  return(<>
    <Routes>
      <Route path='/upload/shows/:id' element={<Shows/>}></Route>
      <Route path='/upload' element={<AddStudent/>}></Route>

    </Routes>
  </>)
}
export default MyApp