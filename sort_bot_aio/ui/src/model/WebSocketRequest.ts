import { z } from "zod"

export default z.object({ "streamCamera": z.boolean().describe("Stream the camera to the client or not").optional() })
