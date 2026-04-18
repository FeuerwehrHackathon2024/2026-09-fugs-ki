import { createCanvasNote, type CanvasDiagramItem, type CanvasImageItem, type CanvasMapItem, type CanvasItem } from "./canvas";

export function createDiagramFactory() {
  return {
    createDiagram: (args: Record<string, any>): CanvasDiagramItem => {
      const layout = args.layout || "flow";
      const nodes = Array.isArray(args.nodes)
        ? args.nodes.map((n: any) => ({
            id: String(n.id || ""),
            label: String(n.label || ""),
            detail: n.detail ? String(n.detail) : undefined,
          }))
        : [];
      const edges = Array.isArray(args.edges)
        ? args.edges.map((e: any) => ({
            from: String(e.from || ""),
            to: String(e.to || ""),
            label: e.label ? String(e.label) : undefined,
          }))
        : [];

      const meta = {
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
      };

      return {
        kind: "diagram",
        title: String(args.title || "Diagramm"),
        summary: String(args.summary || ""),
        layout: layout as "flow" | "radial" | "timeline" | "matrix",
        nodes,
        edges,
        ...meta,
      };
    },
  };
}

export function createMapFactory() {
  return {
    createMap: (args: Record<string, any>): CanvasMapItem => {
      const center = {
        lat: Number(args.center?.lat) || 48.1351,
        lng: Number(args.center?.lng) || 11.582,
      };

      const markers = Array.isArray(args.markers)
        ? args.markers.map((m: any) => ({
            id: String(m.id || ""),
            label: String(m.label || ""),
            point: {
              lat: Number(m.point?.lat) || 0,
              lng: Number(m.point?.lng) || 0,
            },
            kind: (m.kind || "point") as "fire" | "hydrant" | "water" | "vehicle" | "point",
            note: m.note ? String(m.note) : undefined,
          }))
        : [];

      const areas = Array.isArray(args.areas)
        ? args.areas.map((a: any) => ({
            id: String(a.id || ""),
            label: String(a.label || ""),
            center: {
              lat: Number(a.center?.lat) || 0,
              lng: Number(a.center?.lng) || 0,
            },
            radiusMeters: Number(a.radiusMeters) || 100,
            color: a.color ? String(a.color) : undefined,
          }))
        : [];

      const routes = Array.isArray(args.routes)
        ? args.routes.map((r: any) => ({
            id: String(r.id || ""),
            name: String(r.name || ""),
            description: String(r.description || ""),
            points: Array.isArray(r.points)
              ? r.points.map((p: any) => ({
                  lat: Number(p.lat) || 0,
                  lng: Number(p.lng) || 0,
                }))
              : [],
            color: r.color ? String(r.color) : undefined,
          }))
        : [];

      const meta = {
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
      };

      return {
        kind: "map",
        title: String(args.title || "Karte"),
        summary: String(args.summary || ""),
        center,
        zoom: Number(args.zoom) || 12,
        centerLabel: String(args.centerLabel || "Zentrum"),
        layers: Array.isArray(args.layers) ? args.layers.map(String) : [],
        legend: Array.isArray(args.legend) ? args.legend.map(String) : [],
        markers,
        areas,
        routes,
        ...meta,
      };
    },
  };
}

export function createImageFactory() {
  return {
    createImage: (args: Record<string, any>): CanvasImageItem => {
      const meta = {
        id: crypto.randomUUID(),
        createdAt: new Date().toISOString(),
      };

      return {
        kind: "image",
        title: String(args.title || "Bild"),
        summary: String(args.summary || ""),
        sourceUrl: args.sourceUrl ? String(args.sourceUrl) : undefined,
        altText: String(args.altText || ""),
        caption: args.caption ? String(args.caption) : undefined,
        ...meta,
      };
    },
  };
}

export function createNoteFactory() {
  return {
    createNote: (text: string, title = "Notiz", summary = "") => {
      return createCanvasNote(title, summary, text);
    },
  };
}
