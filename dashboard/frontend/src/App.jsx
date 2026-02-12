import React, {useEffect, useState} from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

export default function App(){
  const [prices, setPrices] = useState([])
  const [events, setEvents] = useState([])
  const [cp, setCp] = useState(null)

  useEffect(()=>{
    fetch('/api/prices').then(r=>r.json()).then(data=>{
      // convert to numeric and keep recent
      const parsed = data.map(d=>({date: d.date, price: +d.price})).slice(-2000)
      setPrices(parsed)
    })
    fetch('/api/events').then(r=>r.json()).then(setEvents)
    fetch('/api/change_points').then(r=>r.json()).then(setCp)
  },[])

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h2>Birhan Energies — Brent Price Dashboard</h2>
      <div style={{height:400}}>
        <ResponsiveContainer>
          <LineChart data={prices}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={(d)=>d.slice(0,10)} minTickGap={50}/>
            <YAxis domain={["dataMin","dataMax"]} />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#1f77b4" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{marginTop:20}}>
        <h4>Detected Change Point</h4>
        {cp ? (
          <div>
            <p><b>Model</b>: {cp.model}</p>
            <p><b>Median tau (month)</b>: {cp.tau_median}</p>
            <p><b>mu1</b>: {cp.mu1_mean.toFixed(4)} &nbsp; <b>mu2</b>: {cp.mu2_mean.toFixed(4)}</p>
            <p><b>P(mu2 &gt; mu1)</b>: {cp.p_mu2_gt_mu1}</p>
          </div>
        ) : <p>Loading...</p>}
      </div>

      <div style={{marginTop:20}}>
        <h4>Events (sample)</h4>
        <ul>
          {events.slice(0,10).map((e,i)=>(<li key={i}><b>{e.date}</b> — {e.event}</li>))}
        </ul>
      </div>
    </div>
  )
}
