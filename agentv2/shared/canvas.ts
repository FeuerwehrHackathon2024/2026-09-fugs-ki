export type CanvasItemKind = "diagram" | "image" | "map" | "note";
export type CanvasDiagramLayout = "flow" | "radial" | "timeline" | "matrix";

export interface CanvasDiagramNode {
  id: string;
  label: string;
  detail?: string;
}

export interface CanvasDiagramEdge {
  from: string;
  to: string;
  label?: string;
}

export interface CanvasDiagramItem {
  id: string;
  createdAt: string;
  kind: "diagram";
  title: string;
  summary: string;
  layout: CanvasDiagramLayout;
  nodes: CanvasDiagramNode[];
  edges: CanvasDiagramEdge[];
}

export interface CanvasImageItem {
  id: string;
  createdAt: string;
  kind: "image";
  title: string;
  summary: string;
  sourceUrl?: string;
  altText: string;
  caption?: string;
}

export interface CanvasMapItem {
  id: string;
  createdAt: string;
  kind: "map";
  title: string;
  summary: string;
  center: CanvasGeoPoint;
  zoom: number;
  centerLabel: string;
  layers: string[];
  legend: string[];
  markers: CanvasMapMarker[];
  areas: CanvasMapArea[];
  routes: CanvasMapRoute[];
}

export interface CanvasGeoPoint {
  lat: number;
  lng: number;
}

export interface CanvasMapMarker {
  id: string;
  label: string;
  point: CanvasGeoPoint;
  kind: "fire" | "hydrant" | "water" | "vehicle" | "point";
  note?: string;
}

export interface CanvasMapArea {
  id: string;
  label: string;
  center: CanvasGeoPoint;
  radiusMeters: number;
  color?: string;
}

export interface CanvasMapRoute {
  id: string;
  name: string;
  description: string;
  points: CanvasGeoPoint[];
  color?: string;
}

export interface CanvasNoteItem {
  id: string;
  createdAt: string;
  kind: "note";
  title: string;
  summary: string;
  text: string;
}

export type CanvasItem = CanvasDiagramItem | CanvasImageItem | CanvasMapItem | CanvasNoteItem;

export function createCanvasNote(title: string, summary: string, text: string): CanvasNoteItem {
  return {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    kind: "note",
    title,
    summary,
    text,
  };
}
