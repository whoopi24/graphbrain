package com.graphbrain.webapp

import unfiltered.request._
import unfiltered.response._

import unfiltered.netty._

object GBPlan extends cycle.Plan with cycle.SynchronousExecution with ServerErrorResponse {
  val logger = org.clapper.avsl.Logger(getClass)
  
  def intent = {
    case GET(Path("/")) => 
      logger.debug("GET /")
      ComingSoon()
    case GET(Path("/secret")) => 
      logger.debug("GET /secret")
      Redirect("/node/welcome/graphbrain")
    case GET(Path(Seg("node" :: n1 :: Nil))) => {
      val id = n1 
      logger.debug("GET " + id)
      NodePage(id)
    }
    case GET(Path(Seg("node" :: n1 :: n2 :: Nil))) => {
      val id = n1 + "/" + n2 
      logger.debug("GET " + id)
      NodePage(id)
    }
    case GET(Path(Seg("node" :: n1 :: n2 :: n3 :: Nil))) => {
      val id = n1 + "/" + n2 + "/" + n3
      logger.debug("GET " + id)
      NodePage(id)
    }
    case GET(Path(Seg("node" :: n1 :: n2 :: n3 :: n4 :: Nil))) => {
      val id = n1 + "/" + n2 + "/" + n3 + "/" + n4
      logger.debug("GET " + id)
      NodePage(id)
    }
    case GET(Path(Seg("node" :: n1 :: n2 :: n3 :: n4 :: n5 :: Nil))) => {
      val id = n1 + "/" + n2 + "/" + n3 + "/" + n4 + "/" + n5
      logger.debug("GET " + id)
      NodePage(id)
    }
  }
}
