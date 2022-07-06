import {Wrapper} from "./Wrapper";
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";


export const Products = () => {

    const [products, setProduct] = useState([]);
    
    useEffect(() => {
        (async ()=>{
            const response = await fetch('http://127.0.0.1:8000/products/');
            const content = await response.json(); //all the data is fetched in json format them its setted in content variable
            setProduct(content);
        })();
    },[])

    const del =async id=>{
        if(window.confirm("Delte the item?")){
            await fetch('http://127.0.0.1:8000/products/${id}',{
                method: 'DELETE'
            });
            setProduct(products.filter(p=>p.id !== id));
        }
    }

    return <Wrapper>
        <div className="pt-3 pb-2 mb-3 border-bottom">
        <Link to={`/create`} className="btn btn-sm btn-outline-warning">Add New Products</Link>
        </div>
    
    <div className="table-responsive">
        <table className="table table-striped table-sm">
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Product Id</th>
                <th scope="col">Product Name</th>
                <th scope="col">Product Price</th>
                <th scope="col">Quantity Available</th>
            </tr>
            </thead>
            <tbody>
                {products.map(product =>{ //the product details is mapped now and added in respected field of table
                    return <tr key={product.id}>
                      <td>1,001</td>
              <td>{product.id} </td>
              <td>{product.name}</td>
              <td>{product.price}</td>
              <td>{product.quantity}</td>                              
              <td>
                <a href="#" className="btn btn-s btn-outline-danger" 
                onClick={e=> del(product.id)}>                    
                Delete
                </a>
                </td>                              
              
                    </tr>
                })}
           
               
                  
      </tbody>
     </table>
    </div>
</Wrapper>
}