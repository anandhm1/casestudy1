import React, { Component, useEffect } from 'react';
import axios from 'axios';
import Shows from './show';
import { NavLink } from 'react-router-dom';

class AddStudent extends Component {
  debugger
  state = {
    id: '',
    currency_name:'',
    file1: null
  };
  debugger
  handleChange = (e) => {
    this.setState({
      [e.target.id]: e.target.value
    })
  };

  handlefile1Change = (e) => {
    this.setState({
      file1: e.target.files[0]
    })
  };
  debugger
  handleSubmit = (e) => {
    e.preventDefault();
    console.log(this.state);
    console.log(this.state.id);
    let form_data = new FormData();
    form_data.append('file1', this.state.file1, this.state.file1.name);
    form_data.append('id', this.state.id);
    form_data.append('currency_name', this.state.currency_name);
    let url = 'http://127.0.0.1:8000/company/std/';
    axios.post(url, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }

    })

        .then(res => {
          console.log(res.data);
        })
        .catch(err => console.log(err))
  };
  debugger
  render() {
    return (
      <div className="App">
        <form onSubmit={this.handleSubmit}>
          <p>
            <input type="number" placeholder='id' id='id' value={this.state.id} onChange={this.handleChange} required/>
          </p>
          <p>
            <input type="text" placeholder='currency_name' id='currency_name' value={this.state.currency_name} onChange={this.handleChange} required/>

          </p>
          <p>
            <input type="file"
                   id="file1"
                    onChange={this.handlefile1Change} required/>
          </p>

          <input type="submit" />
        </form>
        <NavLink to={`/upload/shows/${this.state.id}`}><button>Show Data</button></NavLink>
      </div>
    );
  }

}

export default AddStudent;
