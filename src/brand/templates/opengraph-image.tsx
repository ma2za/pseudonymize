import { ImageResponse } from 'next/og'
export const alt = 'pseudonymize.io — Keep the context. Replace the identifiers.'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default function Image() {
  return new ImageResponse(
    <div style={{ width:'100%', height:'100%', display:'flex', flexDirection:'column', justifyContent:'space-between', background:'#0B1013', color:'#F2F6F4', padding:'68px', fontFamily:'Arial, sans-serif' }}>
      <div style={{ fontSize:32, fontWeight:700 }}>pseudonymize<span style={{color:'#5BD6AE'}}>.io</span></div>
      <div style={{ display:'flex', flexDirection:'column', gap:24 }}>
        <div style={{ fontSize:66, lineHeight:1.06, letterSpacing:'-2px', maxWidth:930 }}>Keep the context.<br/>Replace the identifiers.</div>
        <div style={{ display:'flex', gap:16, alignItems:'center', fontFamily:'monospace', fontSize:24 }}>
          <span style={{color:'#A8B5B0'}}>alice@example.com</span><span style={{width:72,height:1,background:'#37474F'}}/><span style={{color:'#5BD6AE'}}>EMAIL_01</span>
        </div>
      </div>
    </div>, size
  )
}
