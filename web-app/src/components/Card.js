import React, {useState,useEffect} from 'react'
import "./Card.css"


export default function Card(props){




    const [count,setCount] = useState(6)
    const [image,setImage] = useState()
    const [question,setQuestion] = useState("")
    const [answer,setAnswer] = useState("Hello World!") 

    const handle_increment = () => {
        setCount(count+1)
        fetch_image()
        setQuestion("")
        setAnswer("")
    }
    const handle_send = () => {
        console.log(question)
        fetch_answer()
    }


    const fetch_image = () => {

        const response = fetch("http://127.0.0.1:5000/fetch_image")
                        .then(response =>{
                            // console.log(response.json())
                            response.json().then((body)=>{

                                // const ImageURL = URL.createObjectURL(new Blob(body['image']));
                                // setImage(ImageURL)
                                setImage(body['image'])
                            }) 


                        })
                        .catch(error => {
                            console.log(error)
                        })

    }

    const fetch_answer = () =>{

            fetch("http://127.0.0.1:5001/get_answer",{
            method: 'POST',
            'headers':{
                'content-type':'application/json',
            },
            'body':JSON.stringify({
                'image':image,
                "question":question
            }),      
        }).then((response)=>{

            response.json().then((body)=>{

                setAnswer(body['answer'])


            })


        })




    }





    useEffect(() =>{

        fetch_image()


    },[])



    return (

        <div className='Card'>
            <div className='card--nav'>

            <button className='NextButton' onClick={handle_increment}>
                Next
            </button>

            </div>
            


            <img src = {`data:image/jpeg;base64,${image}`} alt = "MISSING png"
            className ="card--image"/>
   
            <form>
                <label className='label'>
                    Type in your Question?: 
                </label>
                <input 
                    className= "input-field"
                    type = "text"
                    value = {question}
                    onChange = {(e) => setQuestion(e.target.value)}
                />
            </form>
            <p className='answer'>
            {answer}
            </p>
            <button className='send-button' onClick={handle_send}>
                Send
            </button>

        </div>

    )



}

///// Props 