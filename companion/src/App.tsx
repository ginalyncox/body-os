import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { VitalsPage } from './pages/VitalsPage'
import { FlarePage } from './pages/FlarePage'
import { RespondPage } from './pages/RespondPage'
import { ProtocolPage } from './pages/ProtocolPage'
import { MorePage } from './pages/MorePage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="vitals" element={<VitalsPage />} />
          <Route path="flare" element={<FlarePage />} />
          <Route path="respond" element={<RespondPage />} />
          <Route path="protocol" element={<ProtocolPage />} />
          <Route path="protocol/:tier" element={<ProtocolPage />} />
          <Route path="more" element={<MorePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
