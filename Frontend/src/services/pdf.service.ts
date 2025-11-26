import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import autoTable from 'jspdf-autotable'

async function cloneElementWithCanvasAsImages(element: HTMLElement): Promise<HTMLElement> {
  const clone = element.cloneNode(true) as HTMLElement

  // Find canvases in original and clone and replace clone canvases with img elements
  const origCanvases = Array.from(element.querySelectorAll('canvas'))
  const cloneCanvases = Array.from(clone.querySelectorAll('canvas'))

  for (let i = 0; i < origCanvases.length; i++) {
    const orig = origCanvases[i] as HTMLCanvasElement
    const corresponding = cloneCanvases[i] as HTMLCanvasElement | undefined
    try {
      const dataUrl = orig.toDataURL('image/png')
      if (corresponding && corresponding.parentNode) {
        const img = document.createElement('img')
        img.src = dataUrl
        img.width = corresponding.width
        img.height = corresponding.height
        corresponding.parentNode.replaceChild(img, corresponding)
      }
    } catch (err) {
      // If toDataURL fails (tainted canvas) we skip replacing that canvas
      // and allow html2canvas to try capturing it; keep going.
      // eslint-disable-next-line no-console
      console.warn('No se pudo convertir canvas a imagen:', err)
    }
  }

  return clone
}

export async function exportElementToPdf(element: HTMLElement | null, filename = 'report.pdf') {
  if (!element) throw new Error('Elemento no encontrado para exportar')

  // clonamos y reemplazamos canvases por imágenes para evitar problemas con Chart.js/canvas tainted
  const clone = await cloneElementWithCanvasAsImages(element)

  // posicionar clone fuera de la pantalla para que pueda renderizar estilos
  clone.style.position = 'fixed'
  clone.style.left = '-9999px'
  clone.style.top = '0'
  document.body.appendChild(clone)

  try {
    // If the cloned DOM contains CSS using unsupported color functions (e.g. oklch),
    // skip html2canvas and go directly to fallback (autoTable/textual). This avoids
    // parsing errors inside html2canvas's CSS parser.
    const cloneHtml = (clone && clone.outerHTML) ? clone.outerHTML : ''
    const containsOklch = cloneHtml.includes('oklch')

    try {
      if (containsOklch) {
        // eslint-disable-next-line no-console
        console.warn('Skipping html2canvas because cloned DOM contains unsupported CSS (oklch)')
        throw new Error('contains-oklch')
      }

      const canvas = await html2canvas(clone, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#0f172a', // background similar to app (bg-slate-950)
        logging: false,
      })

      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF('p', 'mm', 'a4')

      // dimensiones en mm
      const pdfWidth = pdf.internal.pageSize.getWidth()
      const pdfHeight = pdf.internal.pageSize.getHeight()

      // obtener dimensiones de la imagen en px
      const imgProps = (pdf as any).getImageProperties(imgData)
      const imgWidth = pdfWidth
      const imgHeight = (imgProps.height * imgWidth) / imgProps.width

      let heightLeft = imgHeight
      let position = 0

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pdfHeight

      while (heightLeft > 0) {
        position = heightLeft - imgHeight
        pdf.addPage()
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
        heightLeft -= pdfHeight
      }

      pdf.save(filename)
      return
    } catch (htmlErr) {
      // html2canvas falló: aplicamos fallback a PDF textual
      // eslint-disable-next-line no-console
      console.error('html2canvas failed, using textual fallback:', htmlErr)
    }

    // Fallback: generar PDF con tablas bien formateadas usando autoTable
    const pdf = new jsPDF('p', 'mm', 'a4')
    const pageWidth = pdf.internal.pageSize.getWidth() - 20 // margen
    const marginLeft = 10

    // Encabezado con título y fecha
    pdf.setFontSize(14)
    pdf.text('Reportes - DeporteX', marginLeft, 16)
    pdf.setFontSize(10)
    const dateStr = new Date().toLocaleString()
    pdf.text(dateStr, pdf.internal.pageSize.getWidth() - marginLeft - pdf.getTextWidth(dateStr), 16)

    const tables = Array.from(clone.querySelectorAll('table'))
    if (tables.length > 0) {
      let startY = 24
      tables.forEach((table) => {
        // extraer encabezados
        const headerRow = table.querySelector('thead tr') || table.querySelector('tr')
        const headers = headerRow
          ? Array.from(headerRow.querySelectorAll('th, td')).map(h => (h.textContent || '').trim())
          : []

        // extraer filas del cuerpo
        const bodyRows: string[][] = []
        const body = table.querySelectorAll('tbody tr')
        const trs = body.length ? Array.from(body) : Array.from(table.querySelectorAll('tr')).slice(1)
        trs.forEach(tr => {
          const cells = Array.from(tr.querySelectorAll('td, th'))
          bodyRows.push(cells.map(c => (c.textContent || '').trim()))
        })

        // use imported autoTable function
        ;(autoTable as any)(pdf, {
          startY,
          head: headers.length ? [headers] : undefined,
          body: bodyRows,
          theme: 'grid',
          headStyles: { fillColor: [16, 185, 129], textColor: 255 },
          styles: { fontSize: 9, cellPadding: 3 },
          margin: { left: marginLeft, right: marginLeft },
        })

        startY = (pdf as any).lastAutoTable ? (pdf as any).lastAutoTable.finalY + 8 : startY + 40
      })
      pdf.save(filename)
      return
    }

    // Si no hay tablas, usar texto plano como fallback
    const text = clone.innerText || clone.textContent || ''
    const lines = pdf.splitTextToSize(text, pageWidth)
    pdf.text(lines, marginLeft, 28)
    pdf.save(filename)
  } finally {
    // siempre eliminar el clone
    if (clone.parentNode) clone.parentNode.removeChild(clone)
  }
}

export default { exportElementToPdf }
