import express from "express";
import { createClient } from "@supabase/supabase-js";
import swaggerUi from "swagger-ui-express";
import swaggerJsdoc from "swagger-jsdoc";

const app = express();
app.use(express.json());

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_KEY!
);

/**
 * @openapi
 * /machines:
 *   get:
 *     summary: Get all machines
 *     responses:
 *       200:
 *         description: List of machines
 */
app.get("/machines", async (_req, res) => {
  const { data, error } = await supabase
    .from("machines")
    .select("*");

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  res.json(data);
});

/**
 * @openapi
 * /machines:
 *   post:
 *     summary: Create a machine
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - status
 *             properties:
 *               name:
 *                 type: string
 *                 example: Machine 004
 *               status:
 *                 type: string
 *                 example: online
 *     responses:
 *       201:
 *         description: Machine created
 */
app.post("/machines", async (req, res) => {
  const { name, status } = req.body;

  const { data, error } = await supabase
    .from("machines")
    .insert({ name, status })
    .select();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  res.status(201).json(data);
});

app.patch("/machines/:id", async (req, res) => {
  const { id } = req.params;

  const { data, error } = await supabase
    .from("machines")
    .update(req.body)
    .eq("id", id)
    .select();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  res.json(data);
});

app.delete("/machines/:id", async (req, res) => {
  const { id } = req.params;

  const { data, error } = await supabase
    .from("machines")
    .delete()
    .eq("id", id)
    .select();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  res.json(data);
});

const port = Number(process.env.PORT) || 3000;

app.listen(port, "0.0.0.0", () => {
  console.log(`Server listening on port ${port}`);
});

const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Machines API",
      version: "1.0.0"
    }
  },
  apis: ["./src/*.ts",
    "./dist/*.js"]
});

app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
