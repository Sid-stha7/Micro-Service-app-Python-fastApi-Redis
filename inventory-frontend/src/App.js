import {Products} from "./components/Products";
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import { ProductCreate } from "./components/ProductsCreate";
import { Orders } from "./components/Orders";


function App() {
    return <BrowserRouter>
        <Routes>
        <Route exact path = "/" element = {<Products/>}/>
        <Route exact path = "/create" element = {<ProductCreate/>}/>
        <Route exact path = "/orders" element = {<Orders/>}/>

        </Routes>
    </BrowserRouter>;
}

export default App;
